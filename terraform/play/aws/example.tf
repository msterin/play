provider "aws" {
  access_key = "AKIAIPGPZCZHRH24WVCA"
  secret_key = "BJmUIjBChHhN38je7ObjtduT6isRgAh9tKO08VVa"
  region     = "us-east-1"
}

resource "aws_instance" "example" {
  ami           = "ami-13be557e"
  instance_type = "t2.micro"
}

