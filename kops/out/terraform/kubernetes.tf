provider "aws" {
  region = "us-east-2"
}

resource "aws_autoscaling_group" "master-us-east-2b-masters-k2-awsplay-sterinfamily-com" {
  name                 = "master-us-east-2b.masters.k2.awsplay.sterinfamily.com"
  launch_configuration = "${aws_launch_configuration.master-us-east-2b-masters-k2-awsplay-sterinfamily-com.id}"
  max_size             = 1
  min_size             = 1
  vpc_zone_identifier  = ["${aws_subnet.us-east-2b-k2-awsplay-sterinfamily-com.id}"]

  tag = {
    key                 = "KubernetesCluster"
    value               = "k2.awsplay.sterinfamily.com"
    propagate_at_launch = true
  }

  tag = {
    key                 = "Name"
    value               = "master-us-east-2b.masters.k2.awsplay.sterinfamily.com"
    propagate_at_launch = true
  }

  tag = {
    key                 = "k8s.io/role/master"
    value               = "1"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_group" "nodes-k2-awsplay-sterinfamily-com" {
  name                 = "nodes.k2.awsplay.sterinfamily.com"
  launch_configuration = "${aws_launch_configuration.nodes-k2-awsplay-sterinfamily-com.id}"
  max_size             = 2
  min_size             = 2
  vpc_zone_identifier  = ["${aws_subnet.us-east-2b-k2-awsplay-sterinfamily-com.id}"]

  tag = {
    key                 = "KubernetesCluster"
    value               = "k2.awsplay.sterinfamily.com"
    propagate_at_launch = true
  }

  tag = {
    key                 = "Name"
    value               = "nodes.k2.awsplay.sterinfamily.com"
    propagate_at_launch = true
  }

  tag = {
    key                 = "k8s.io/role/node"
    value               = "1"
    propagate_at_launch = true
  }
}

resource "aws_ebs_volume" "b-etcd-events-k2-awsplay-sterinfamily-com" {
  availability_zone = "us-east-2b"
  size              = 20
  type              = "gp2"
  encrypted         = false

  tags = {
    KubernetesCluster    = "k2.awsplay.sterinfamily.com"
    Name                 = "b.etcd-events.k2.awsplay.sterinfamily.com"
    "k8s.io/etcd/events" = "b/b"
    "k8s.io/role/master" = "1"
  }
}

resource "aws_ebs_volume" "b-etcd-main-k2-awsplay-sterinfamily-com" {
  availability_zone = "us-east-2b"
  size              = 20
  type              = "gp2"
  encrypted         = false

  tags = {
    KubernetesCluster    = "k2.awsplay.sterinfamily.com"
    Name                 = "b.etcd-main.k2.awsplay.sterinfamily.com"
    "k8s.io/etcd/main"   = "b/b"
    "k8s.io/role/master" = "1"
  }
}

resource "aws_iam_instance_profile" "masters-k2-awsplay-sterinfamily-com" {
  name  = "masters.k2.awsplay.sterinfamily.com"
  roles = ["${aws_iam_role.masters-k2-awsplay-sterinfamily-com.name}"]
}

resource "aws_iam_instance_profile" "nodes-k2-awsplay-sterinfamily-com" {
  name  = "nodes.k2.awsplay.sterinfamily.com"
  roles = ["${aws_iam_role.nodes-k2-awsplay-sterinfamily-com.name}"]
}

resource "aws_iam_role" "masters-k2-awsplay-sterinfamily-com" {
  name               = "masters.k2.awsplay.sterinfamily.com"
  assume_role_policy = "${file("${path.module}/data/aws_iam_role_masters.k2.awsplay.sterinfamily.com_policy")}"
}

resource "aws_iam_role" "nodes-k2-awsplay-sterinfamily-com" {
  name               = "nodes.k2.awsplay.sterinfamily.com"
  assume_role_policy = "${file("${path.module}/data/aws_iam_role_nodes.k2.awsplay.sterinfamily.com_policy")}"
}

resource "aws_iam_role_policy" "masters-k2-awsplay-sterinfamily-com" {
  name   = "masters.k2.awsplay.sterinfamily.com"
  role   = "${aws_iam_role.masters-k2-awsplay-sterinfamily-com.name}"
  policy = "${file("${path.module}/data/aws_iam_role_policy_masters.k2.awsplay.sterinfamily.com_policy")}"
}

resource "aws_iam_role_policy" "nodes-k2-awsplay-sterinfamily-com" {
  name   = "nodes.k2.awsplay.sterinfamily.com"
  role   = "${aws_iam_role.nodes-k2-awsplay-sterinfamily-com.name}"
  policy = "${file("${path.module}/data/aws_iam_role_policy_nodes.k2.awsplay.sterinfamily.com_policy")}"
}

resource "aws_internet_gateway" "k2-awsplay-sterinfamily-com" {
  vpc_id = "${aws_vpc.k2-awsplay-sterinfamily-com.id}"

  tags = {
    KubernetesCluster = "k2.awsplay.sterinfamily.com"
    Name              = "k2.awsplay.sterinfamily.com"
  }
}

resource "aws_key_pair" "kubernetes-k2-awsplay-sterinfamily-com-7c770830be27901f388e1e2e31d6d6f3" {
  key_name   = "kubernetes.k2.awsplay.sterinfamily.com-7c:77:08:30:be:27:90:1f:38:8e:1e:2e:31:d6:d6:f3"
  public_key = "${file("${path.module}/data/aws_key_pair_kubernetes.k2.awsplay.sterinfamily.com-7c770830be27901f388e1e2e31d6d6f3_public_key")}"
}

resource "aws_launch_configuration" "master-us-east-2b-masters-k2-awsplay-sterinfamily-com" {
  name_prefix                 = "master-us-east-2b.masters.k2.awsplay.sterinfamily.com-"
  image_id                    = "ami-35664350"
  instance_type               = "c4.large"
  key_name                    = "${aws_key_pair.kubernetes-k2-awsplay-sterinfamily-com-7c770830be27901f388e1e2e31d6d6f3.id}"
  iam_instance_profile        = "${aws_iam_instance_profile.masters-k2-awsplay-sterinfamily-com.id}"
  security_groups             = ["${aws_security_group.masters-k2-awsplay-sterinfamily-com.id}"]
  associate_public_ip_address = true
  user_data                   = "${file("${path.module}/data/aws_launch_configuration_master-us-east-2b.masters.k2.awsplay.sterinfamily.com_user_data")}"

  root_block_device = {
    volume_type           = "gp2"
    volume_size           = 20
    delete_on_termination = true
  }

  lifecycle = {
    create_before_destroy = true
  }
}

resource "aws_launch_configuration" "nodes-k2-awsplay-sterinfamily-com" {
  name_prefix                 = "nodes.k2.awsplay.sterinfamily.com-"
  image_id                    = "ami-35664350"
  instance_type               = "t2.medium"
  key_name                    = "${aws_key_pair.kubernetes-k2-awsplay-sterinfamily-com-7c770830be27901f388e1e2e31d6d6f3.id}"
  iam_instance_profile        = "${aws_iam_instance_profile.nodes-k2-awsplay-sterinfamily-com.id}"
  security_groups             = ["${aws_security_group.nodes-k2-awsplay-sterinfamily-com.id}"]
  associate_public_ip_address = true
  user_data                   = "${file("${path.module}/data/aws_launch_configuration_nodes.k2.awsplay.sterinfamily.com_user_data")}"

  root_block_device = {
    volume_type           = "gp2"
    volume_size           = 20
    delete_on_termination = true
  }

  lifecycle = {
    create_before_destroy = true
  }
}

resource "aws_route" "0-0-0-0--0" {
  route_table_id         = "${aws_route_table.k2-awsplay-sterinfamily-com.id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.k2-awsplay-sterinfamily-com.id}"
}

resource "aws_route_table" "k2-awsplay-sterinfamily-com" {
  vpc_id = "${aws_vpc.k2-awsplay-sterinfamily-com.id}"

  tags = {
    KubernetesCluster = "k2.awsplay.sterinfamily.com"
    Name              = "k2.awsplay.sterinfamily.com"
  }
}

resource "aws_route_table_association" "us-east-2b-k2-awsplay-sterinfamily-com" {
  subnet_id      = "${aws_subnet.us-east-2b-k2-awsplay-sterinfamily-com.id}"
  route_table_id = "${aws_route_table.k2-awsplay-sterinfamily-com.id}"
}

resource "aws_security_group" "masters-k2-awsplay-sterinfamily-com" {
  name        = "masters.k2.awsplay.sterinfamily.com"
  vpc_id      = "${aws_vpc.k2-awsplay-sterinfamily-com.id}"
  description = "Security group for masters"

  tags = {
    KubernetesCluster = "k2.awsplay.sterinfamily.com"
    Name              = "masters.k2.awsplay.sterinfamily.com"
  }
}

resource "aws_security_group" "nodes-k2-awsplay-sterinfamily-com" {
  name        = "nodes.k2.awsplay.sterinfamily.com"
  vpc_id      = "${aws_vpc.k2-awsplay-sterinfamily-com.id}"
  description = "Security group for nodes"

  tags = {
    KubernetesCluster = "k2.awsplay.sterinfamily.com"
    Name              = "nodes.k2.awsplay.sterinfamily.com"
  }
}

resource "aws_security_group_rule" "all-master-to-master" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.masters-k2-awsplay-sterinfamily-com.id}"
  source_security_group_id = "${aws_security_group.masters-k2-awsplay-sterinfamily-com.id}"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
}

resource "aws_security_group_rule" "all-master-to-node" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.nodes-k2-awsplay-sterinfamily-com.id}"
  source_security_group_id = "${aws_security_group.masters-k2-awsplay-sterinfamily-com.id}"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
}

resource "aws_security_group_rule" "all-node-to-node" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.nodes-k2-awsplay-sterinfamily-com.id}"
  source_security_group_id = "${aws_security_group.nodes-k2-awsplay-sterinfamily-com.id}"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
}

resource "aws_security_group_rule" "https-external-to-master-0-0-0-0--0" {
  type              = "ingress"
  security_group_id = "${aws_security_group.masters-k2-awsplay-sterinfamily-com.id}"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "master-egress" {
  type              = "egress"
  security_group_id = "${aws_security_group.masters-k2-awsplay-sterinfamily-com.id}"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "node-egress" {
  type              = "egress"
  security_group_id = "${aws_security_group.nodes-k2-awsplay-sterinfamily-com.id}"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "node-to-master-tcp-4194" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.masters-k2-awsplay-sterinfamily-com.id}"
  source_security_group_id = "${aws_security_group.nodes-k2-awsplay-sterinfamily-com.id}"
  from_port                = 4194
  to_port                  = 4194
  protocol                 = "tcp"
}

resource "aws_security_group_rule" "node-to-master-tcp-443" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.masters-k2-awsplay-sterinfamily-com.id}"
  source_security_group_id = "${aws_security_group.nodes-k2-awsplay-sterinfamily-com.id}"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
}

resource "aws_security_group_rule" "ssh-external-to-master-0-0-0-0--0" {
  type              = "ingress"
  security_group_id = "${aws_security_group.masters-k2-awsplay-sterinfamily-com.id}"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "ssh-external-to-node-0-0-0-0--0" {
  type              = "ingress"
  security_group_id = "${aws_security_group.nodes-k2-awsplay-sterinfamily-com.id}"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_subnet" "us-east-2b-k2-awsplay-sterinfamily-com" {
  vpc_id            = "${aws_vpc.k2-awsplay-sterinfamily-com.id}"
  cidr_block        = "172.20.32.0/19"
  availability_zone = "us-east-2b"

  tags = {
    KubernetesCluster = "k2.awsplay.sterinfamily.com"
    Name              = "us-east-2b.k2.awsplay.sterinfamily.com"
  }
}

resource "aws_vpc" "k2-awsplay-sterinfamily-com" {
  cidr_block           = "172.20.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    KubernetesCluster = "k2.awsplay.sterinfamily.com"
    Name              = "k2.awsplay.sterinfamily.com"
  }
}

resource "aws_vpc_dhcp_options" "k2-awsplay-sterinfamily-com" {
  domain_name         = "us-east-2.compute.internal"
  domain_name_servers = ["AmazonProvidedDNS"]

  tags = {
    KubernetesCluster = "k2.awsplay.sterinfamily.com"
    Name              = "k2.awsplay.sterinfamily.com"
  }
}

resource "aws_vpc_dhcp_options_association" "k2-awsplay-sterinfamily-com" {
  vpc_id          = "${aws_vpc.k2-awsplay-sterinfamily-com.id}"
  dhcp_options_id = "${aws_vpc_dhcp_options.k2-awsplay-sterinfamily-com.id}"
}
