# Deploying an application to Amazon EKS

## Prerequisites

### Create an Amazon Web Services (AWS) account  
If you already have an account, skip this step.  
1. Go to this [link](https://portal.aws.amazon.com/billing/signup) and follow the instructions.  
You will need a valid debit or credit card. You will not be charged, it is only to validate your ID.  
  
### Install AWS Command Line Interface (AWSCLI)  
  
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
  
### Install `eksctl`
If you have already installed the `eksctl` tool previously, please update to the latest version so that your `GitTag` is `0.12.0`.  
  
1. Follow the instructions [here](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html#w243aac11b7b5b9b7b1) under the "**Install eksctl**" section to install _eksctl_ depending on your operating system.  
  
If you run `eksctl version` in your Terminal window, you should get `version.Info{BuiltAt:"", GitCommit:"", GitTag:"0.12.0"}`. The `GitTag` should be `0.12.0`.  
   
### Install `kubectl`  
  
1. Install the Kubernetes command-line tool, [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/), so that you can communicate with Kubernetes clusters.  
	* Follow the instructions in the link to install the proper version depending on your operating system (Linux, MacOS, or Windows). Either versions `v1.16.0` or `v1.17.0` are fine. You can choose to install through a package manager (like Homebrew) or by downloading the binary.  
  
### Install Postman  
Follow the instructions of your operating system:  
* [macOS](https://learning.getpostman.com/docs/postman/launching-postman/installation-and-updates/#installing-postman-on-mac)  
* [Windows](https://learning.getpostman.com/docs/postman/launching-postman/installation-and-updates/#installing-postman-on-windows)  
* [Linux](https://learning.getpostman.com/docs/postman/launching-postman/installation-and-updates/#installing-postman-on-linux)  


## 1. Build a Docker image for application

We will now put our sentiment analysis Flask application into a Docker container.

1. Let's create a Docker container for our Flask application.
    1. Change directories into the `2020-ComputeFest/notebook_to_cloud/ml_deploy_demo/` directory.
    2. Run `docker build -t <your_Dockerhub_username>/sentiment-analysis:latest -f Dockerfile .`
    3. Run `docker image ls` to see that we created a new Docker image with the tag `server`.
    4. Run `docker run -it --rm -p 5000:5000 <your_Dockerhub_username>/sentiment-analysis:latest /bin/bash ml_deploy_demo/run.sh`.
        2. By using the `-p 5000:5000` flag, we expose port 8080 to the outside so our web page can be accessed.
2. Use [Postman](https://www.getpostman.com/downloads/) to hit the endpoint at http://0.0.0.0:5000/predict.
    1. Please send a `POST` request to the URL above.
    2. Click on the *Body* tab, change the selection to *raw*, and change the format from *Text* to *JSON*.
    3. Enter the following code into the text area:
```
{"data":  ["this place is the worst!",
            "this place is the best!",
            "I love this place!"]}
```
    
    4. Hit *Send* and you should get a response identical to the text below:
```
{
    "input": {
        "data": [
            "this place is the worst!",
            "this place is the best!",
            "I love this place!"
        ]
    },
    "pred": [
        [
            0.07278868556022644
        ],
        [
            0.8637552857398987
        ],
        [
            0.42799580097198486
        ]
    ]
}
```

3. Push your image to your DockerHub repo using `docker push <your_Dockerhub_username>/sentiment-analysis:latest`.
4. Clean-up steps:
    1. Stop your containers with `docker stop $(docker container ls -q)`. This may take a few seconds.
    2. Delete your containers with `docker rm $(docker ps -aq)`. Beware, this will stop all containers you have running on your computer, so if you have containers running for other classes, you will have to remove the containers using the container IDs.
    3. Use `docker rmi <IMAGE_ID>` to delete your images, if you would like to.
    
## 2. Deploy your container to an EKS Cluster

### Create an EKS cluster
1. From the `2020-ComputeFest/notebook_to_cloud/ml_deploy_demo/kubernetes/` directory, run `eksctl create cluster -f cluster.yaml` to create an EKS cluster on AWS.
    1. This will take 10-15 minutes.
2. Once this is done, run `kubectl get nodes` to make sure your `kubectl` is configured to communicate with the cluster you just created.
    1. You should see 2 IP addresses with **Status** as *Ready*.
    
### Deploy Flask application on cluster
3. We can create a deployment for our Docker image using `kubectl create -f sentiment_analysis_deployment.yaml`.
    1. Change the `image` field to the name of the image you pushed to your repository.
    2. After a few seconds, run `kubectl get po` to see the pod you just created for your Flask application. The **Status** should saying *Running*. If the **Status** is not *Running*, wait a few more seconds and run `kubectl get po` again.
4. We can create a service for our running pod using `kubectl create -f sentiment_analysis_service.yaml`.
    1. After a few seconds, run `kubectl get svc` to see the service you just created for your Flask application.
    2. You should see a link under **EXTERNAL-IP** that looks similar to  
    `ab0ffcc67371d11eabbec0249b21ade2-2082982831.us-east-1.elb.amazonaws.com`.
5. Use Postman to send a `POST` request to `http://<link_from_step_4B>:5000/predict` with a JSON body that contains  
`{"data":  ["this place is the worst!", "this place is the best!", "I hate this place."]}`.

### Clean-up app and delete cluster
**WARNING: If you do not delete your cluster, you will get charged extra by AWS.**  

6. Run `kubectl delete -f sentiment_analysis_service.yaml` to delete the service. This deletes the *LoadBalancer*, which prevents anyone from accessing the application from the outside world.
    1. Verify this by running `kubectl get svc`. You should no longer see the *sentiment-analysis-service*.  
7. Run `kubectl delete -f sentiment_analysis_deployment.yaml` to delete the pod holding our Docker container. Our application is no longer running on the EKS cluster.  
    1. Verify this by running `kubectl get po`. You may see that the **STATUS** of your pod is *Terminating* or a message saying "*No resources found in default namespace.*".  
8. Run `eksctl delete cluster -f cluster.yaml` to delete your EKS cluster.  
    1. This will take 10-15 minutes.  