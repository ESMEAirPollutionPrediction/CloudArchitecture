resource "local_file" "ssh-connect-bat" {
    filename = "../bin/ssh_connect.bat"
    content = "ssh -i \"~/.ssh/ec2\" ec2-user@${aws_instance.my-ec2.public_dns}"
}

resource "local_file" "ssh-connect-sh" {
    filename = "../bin/ssh_connect.sh"
    content = "#!/bin/bash\nssh -i \"~/.ssh/ec2\" ec2-user@${aws_instance.my-ec2.public_dns}"
}