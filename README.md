
[https://github.com/Harvard-IACS/2020-ComputeFest/](https://github.com/Harvard-IACS/2020-ComputeFest/)  

  

# Install instructions  
  
  
  
## Create an Amazon Web Services (AWS) account  
If you already have an account, skip this step.  
1. Go to this [link](https://portal.aws.amazon.com/billing/signup) and follow the instructions.  
You will need a valid debit or credit card. You will not be charged, it is only to validate your ID.  
  
## Install AWS Command Line Interface (AWSCLI)  
  
1. Install the AWS CLI **Version 1** for your operating system. Please follow the appropriate link below based on your operating system.  
* [Linux](https://docs.aws.amazon.com/cli/latest/userguide/install-linux.html)  
* [macOS](https://docs.aws.amazon.com/cli/latest/userguide/install-macos.html)  
* [Windows](https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html#install-msi-on-windows)  
\* Please make sure you add the AWS CLI version 1 executable to your command line Path.  
  
Verify that AWS CLI is installed correctly by running `aws --version`.  
* You should see something similar to `aws-cli/1.17.0 Python/3.7.4 Darwin/18.7.0 botocore/1.14.0`.  
  
#### Configuring the AWS CLI  
You need to retrieve AWS credentials that allow your AWS CLI to access AWS resources.  
  
1. Sign into the [AWS console]([https://aws.amazon.com/console/](https://aws.amazon.com/console/)). This simply requires that you sign in with the email and password you used to create your account. If you already have an AWS account, be sure to log in as the _root user_.  
2. Choose your account name in the navigation bar at the top right, and then choose **My Security Credentials**.  
3. Expand the **Access keys (access key ID and secret access key)** section.  
4. Press **Create New Access Key**.  
5. Press **Download Key File** to download a CSV file that contains your new _AccessKeyId_ and _SecretKey_. Keep this file somewhere where you can find it easily.  
  
Now, you can configure your AWS CLI with the credentials you just created and downloaded.  
  
1. In your Terminal, run `aws configure`.  
  
	i. Enter your _AWS Access Key ID_ from the file you downloaded.  
	ii. Enter the _AWS Secret Access Key_ from the file.  
	iii. For _Default region name_, enter ``us-east-1``.  
	iv. For _Default output format_, enter ``json``.  
  
2. Run `aws s3 ls` in your Terminal. If your AWS CLI is configured correctly, you should see nothing (because you do not have any existing AWS S3 buckets) or if you have created AWS S3 buckets before, they will be listed in your Terminal window.  
  
\* If you get an error, then please try to configure your AWS CLI again.  
  
## Install `eksctl`
If you have already installed the `eksctl` tool previously, please update to the latest version so that your `GitTag` is `0.12.0`.  
  
1. Follow the instructions [here]([https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html#w243aac11b7b5b9b7b1](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html#w243aac11b7b5b9b7b1)) under the "**Install eksctl**" section to install _eksctl_ depending on your operating system.  
  
If you run `eksctl version` in your Terminal window, you should get `version.Info{BuiltAt:"", GitCommit:"", GitTag:"0.12.0"}`. The `GitTag` should be `0.12.0`.  
  
  
  
## Install `kubectl`  
  
1. Install the Kubernetes command-line tool, [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/), so that you can communicate with Kubernetes clusters.  
	* Follow the instructions in the link to install the proper version depending on your operating system (Linux, MacOS, or Windows). Either versions `v1.16.0` or `v1.17.0` are fine. You can choose to install through a package manager (like Homebrew) or by downloading the binary.  
  
## Install Postman  
Follow the instructions of your operating system:  
* [macOS](https://learning.getpostman.com/docs/postman/launching-postman/installation-and-updates/#installing-postman-on-mac)  
* [Windows](https://learning.getpostman.com/docs/postman/launching-postman/installation-and-updates/#installing-postman-on-windows)  
* [Linux](https://learning.getpostman.com/docs/postman/launching-postman/installation-and-updates/#installing-postman-on-linux)  
  
## Install Docker  
  
1. Install `Docker Desktop`. Use one of the links below to download the proper Docker application depending on your operating system. Create a DockerHub account if asked.  
* For macOS, follow this [link](https://docs.docker.com/docker-for-mac/install/).  
* For Linux, follow this [link](https://docs.docker.com/install/linux/docker-ce/ubuntu/).  
* For Windows 10 64-bit (Pro, Enterprise, or Education), follow this [link](https://docs.docker.com/docker-for-windows/install/).  
* For Windows 10 64-bit Home:
	1. Excecute the files "first.bat" and "second.bat" in order, as administrator.
	2. Restart your computer.
	3. Excecute the following commands in terminal, as administrator.
	
			REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /f /v EditionID /t REG_SZ /d "Professional"
			REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /f /v ProductName /t REG_SZ /d "Windows 10 Pro"
	4. Follow this [link](https://docs.docker.com/docker-for-windows/install/) to install Docker.
	5.	Restart your computer, do not log out.
	6.	Excecute the following commands in terminal, as administrator.
	
			REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v EditionID /t REG_SZ /d "Core"
			REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v ProductName /t REG_SZ /d "Windows 10 Home"
  
Open a Terminal window and type  `docker run hello-world`  to make sure Docker is installed  properly . 
	It should appear the following message:
	
	`` Hello from Docker!``  
	``This message shows that your installation appears to be working correctly.``
	
Finally, in the Terminal window excecute ``docker pull tensorflow/tensorflow:2.1.0-py3-jupyter``.

## Install Anaconda  
  
Follow the instructions for your operating system.  
* For macOS, follow this [link](https://docs.anaconda.com/anaconda/install/mac-os/).  
* For Windows, follow this [link](https://docs.anaconda.com/anaconda/install/windows/).  
* For Linux, follow this [link](https://docs.anaconda.com/anaconda/install/linux/).  
  
## Install Sublime  
Follow the [instructions](https://www.sublimetext.com/3) for your operating system.  
If you already have a prefered text editor, skip this step.  
  
  
## Clone the github repository  
  
Clone or download [this repository](https://github.com/Harvard-IACS/2020-ComputeFest/).
