# Create instance
[Terraform Tutorials - HashiCorp Learn](https://learn.hashicorp.com/terraform)

AWS:

1. intall Terraform
2. Build Infrastructure

在amazon china的users-> summary -> security credentials可以创建access key id

通过aws configure命令配置key



在main.tf文件里将 region设置为 cn-north-1

~~通过命令：~~

~~aws ec2 describe-images --owners self amazon --filters "Name=root-device-type,Values=ebs"~~

从[Ubuntu Amazon EC2 AMI Finder](https://cloud-images.ubuntu.com/locator/ec2/) 找找到 "ImageId"， 填入main.tf





创建实例的同时，创建ssh登陆用的key-pair及pem:

[Create a key pair and download the .pem file with Terraform (AWS)](https://stackoverflow.com/questions/67389324/create-a-key-pair-and-download-the-pem-file-with-terraform-aws)



```plain
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "cn-north-1"
}

resource "aws_instance" "app_server" {
  ami           = "ami-03bd5b54f08201029"
  instance_type = "t2.micro"
  key_name = "myKey"

  tags = {
    Name = "TestInstance"
    # Name = var.instance_name
  }
}

resource "tls_private_key" "pk" {
  algorithm = "RSA"
  rsa_bits  = 4096
}


resource "aws_key_pair" "kp" {
  key_name   = "myKey"
  public_key = tls_private_key.pk.public_key_openssh

  provisioner "local-exec" { # Create a "myKey.pem" to your computer!!
    command = "echo '${tls_private_key.pk.private_key_pem}' > ./myKey.pem"
  }
}
```



找到instance的security group, 在inbound rules里添加ssh登陆许可


# bandwith test
1. install iperf to intance

```python
sudo apt install iperf 
```

2. start server on instance

```python
iperf -s 
```

3. run command on client side
```python
iperf -c 52.81.228.31
```

