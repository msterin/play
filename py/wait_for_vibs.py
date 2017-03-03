#!/usr/bin/env python
# Copyright 2016 VMware, Inc. All Rights Reserved.

# checking how to get VIBs (and wait for tasks, maybe for Host PowerOff)
import ssl

import pyVim
import pyVmomi
from pyVim.connect import Connect, Disconnect

from pyVmomi import VmomiSupport, vim, vmodl
# from pyVim import host

def getTaskList(prop_collector, tasks):
    # Create filter
    obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                 for task in tasks]
    property_spec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task,
                                                               pathSet=[],
                                                               all=True)
    filter_spec = vmodl.query.PropertyCollector.FilterSpec()
    filter_spec.objectSet = obj_specs
    filter_spec.propSet = [property_spec]
    return prop_collector.CreateFilter(filter_spec, True)



def wait_for_tasks(si, tasks):
    """Given the service instance si and tasks, it returns after all the
   tasks are complete
   """
    task_list = [str(task) for task in tasks]
    property_collector = si.content.propertyCollector
    pcfilter = getTaskList(property_collector, tasks)

    try:
        version, state = None, None
        # Loop looking for updates till the state moves to a completed state.
        while len(task_list):
            update = property_collector.WaitForUpdates(version)
            for filter_set in update.filterSet:
                for obj_set in filter_set.objectSet:
                    task = obj_set.obj
                    for change in obj_set.changeSet:
                        if change.name == 'info':
                            state = change.val.state
                        elif change.name == 'info.state':
                            state = change.val
                        else:
                            continue

                        if not str(task) in task_list:
                            continue

                        if state == vim.TaskInfo.State.success:
                            # Remove task from taskList
                            task_list.remove(str(task))
                        elif state == vim.TaskInfo.State.error:
                            raise task.info.error
            # Move to next version
            version = update.version
    finally:
        if pcfilter:
            pcfilter.Destroy()


def get_info():
    endpoint, user, pwd ='172.16.245.151', 'root', 'ca$hc0w'
    print("connecting to", endpoint, user, pwd)

    si = pyVim.connect.Connect(host=endpoint, user=user, pwd=pwd,
                               sslContext=ssl._create_unverified_context())
    print("Connected")
    # patch_manager = host.GetHostSystem(si).configManager.patchManager
    # task = patch_manager.QueryHostPatch_Task()
    # try:
    #     wait_for_tasks(si, [task])
    # except:
    #     print("wait for tasks failed")
    #
    # print ("DONE")
    # print ("result ", task.info.result)
    # print ("info", task.info)
    # print ("task", task)
    return si



def wait_for_events_loop(service_instance):
    content = service_instance.RetrieveContent()

    # Create a container view
    container_view = content.viewManager.CreateContainerView(
        container=content.rootFolder,
        type=[pyVmomi.vim.HostSystem],
        recursive=True)

    # Create a traversal spec
    traversal_spec = pyVmomi.vim.PropertyCollector.TraversalSpec(
        name='traversal_spec',
        path='view',
        skip=False,
        type=pyVmomi.vim.view.ContainerView)

    # Create an object spec
    object_spec = pyVmomi.vim.PropertyCollector.ObjectSpec(
        obj=container_view,
        selectSet=[traversal_spec],
        skip=False)

    # Create a property specs for host events
    property_spec_host_events = pyVmomi.vim.PropertyCollector.PropertySpec(
        all=False,
        pathSet=["runtime.powerState"],
        type=pyVmomi.vim.HostSystem)

    # Create a property filter spec
    property_filter_spec = pyVmomi.vim.PropertyCollector.FilterSpec(
        objectSet=[object_spec],
        propSet=[property_spec_host_events],
        reportMissingObjectsInResults=True)

    # Create the property filter
    content.propertyCollector.CreateFilter(
        spec=property_filter_spec,
        partialUpdates=True)

    # Set up the wait options
    max_wait = 10
    wait_options = pyVmomi.vim.PropertyCollector.WaitOptions(
        maxWaitSeconds=max_wait,
        maxObjectUpdates=None)

    # Initialize update version and start time
    update_version = None

    # Loop until exit flag has been set
    while True:
        # Block until an update is received or timeout is received
        update_set = content.propertyCollector.WaitForUpdatesEx(
            version=update_version,
            options=wait_options)

        if update_set is None:
            print("Timeout/Requery")

            # Reset the update version number to force a full requery.
            update_version = None

        else:
            print("  Received Update (v{})".format(update_set.version))
            update_version = update_set.version

        print("")


# from vmware.esximage import HostImage # needed for dealing with esxcli
# start the server
if __name__ == "__main__":
    si = get_info()
    wait_for_events_loop(si)
