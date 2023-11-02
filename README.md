<h1 align="center">Naver Cloud Collector</h1>  

<br/>  
<div align="center" style="display:flex;">  
  <a href='https://www.ncloud.com/'><img width="320" src="https://www.dotnetpia.co.kr/wp-content/uploads/2021/04/ncp-logo-3-8.png"></a>  
  <p> 
    <br>
    <img alt="Version"  src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000"  />  
    <a href="https://www.apache.org/licenses/LICENSE-2.0"  target="_blank"><img alt="License: Apache 2.0"  src="https://img.shields.io/badge/License-Apache 2.0-yellow.svg" /></a> 
  </p> 
</div>    

**Plugin to collect Naver Cloud**

> SpaceONE's [plugin-naver-cloud-inven-collector](https://github.com/kiku99/plugin-naver-cloud-service-inven-collector) is a convenient tool to
get cloud service data from Naver Cloud platform.



Please contact us if you need any further information. (<elsd0326@gmail.com>)

---


### Service list

The following is a list of services being collected and service code information.

|No.| Service name   | Service Code |
|---|----------------|--------------|
|1| Server         | compute|
|2| Autoscaling    |compute|
|3| Cloud DB       |database|
|4| Object Storage |storage|
|5| Archive Storage |storage|
|6| VPC            |networking|
|7| Monitoring     |management|
|8| CDN            |content delivery|



<br>
<br>

### Content details

* Table of Contents
    * [Compute](#compute)
        * [Server](#server)
        * [Autoscaling](#autoscaling)

    * [Database](#database)
        * [Cloud DB](#cloud-db)
  
    * [Storage](#storage)
        * [Object Storage](#object-storage)
        * [Archive Storage](#archive-storage)
  
    * [Networking](#networking)
        * [Vpc](#vpc)
  
    * [Management](#management)
        * [Monitoring](#monitoring)
  
    * [Content Delivery](#content-delivery)
        * [Cdn](#cdn)
<br>

---
## SETTING
You should insert information about account in Cloudforet's **Service Account** initially.
* Credentials
	* `ncloud_access_key_id`
	* `ncloud_secret_key`
	* `domain_id`
	* `project_id`
* Options
  * `db_kind_code`  
  * `cdn_instance_no` 
  * `instance_no`
  * `bucket_name` 
---

## Authentication Overview
Registered service account on SpaceONE must have certain permissions to collect cloud service data
Please, set authentication privilege for followings:

#### Compute

- ##### [Server](https://api.ncloud-docs.com/docs/compute-server)
    - Scopes
        - https://api.ncloud-docs.com/docs/compute-server-getserverinstancelist
        - https://api.ncloud-docs.com/docs/compute-server-getblockstorageinstancelist
        - https://api.ncloud-docs.com/docs/compute-server-getloginkeylist
     
    - IAM
        - compute.serverinstance.list
        - compute.blockstorageinstance.list
        - compute.loginkey.list

- ##### [Autoscaling](https://api.ncloud-docs.com/docs/compute-autoscaling)
    - Scopes
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getadjustmenttypelist
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getautoscalingactivityloglist
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getautoscalingconfigurationloglist
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getautoscalingpolicylist
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getlaunchconfigurationlist
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getscalingprocesstypelist
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getscheduledactionlist
     
     - IAM
        - compute.adjustmenttype.list
        - compute.autoscalingactivitylog.list
        - compute.autoscalingconfiguration.list
        - compute.autoscalingpolicy.list
        - compute.launchconfiguration.list
        - compute.scalingprocesstype.list
        - compute.scheuleaction.list
     

#### Database     
- ##### [Cloud DB](https://api.ncloud-docs.com/docs/database-clouddb)
    - Scopes
        - https://api.ncloud-docs.com/docs/database-clouddb-getclouddbinstancelist
        - https://api.ncloud-docs.com/docs/database-clouddb-getclouddbconfiggrouplist
        - https://api.ncloud-docs.com/docs/database-clouddb-getclouddbimageproductlist
        - https://api.ncloud-docs.com/docs/database-clouddb-getclouddbproductlist
        - https://api.ncloud-docs.com/docs/database-clouddb-getbackuplist
        - https://api.ncloud-docs.com/docs/database-clouddb-getdmsoperation
        - https://api.ncloud-docs.com/docs/database-clouddb-getobjectstoragebackuplist
     
    - IAM
        - database.clouddbinstance.list
        - database.autoscalingactivitylog.list
        - database.autoscalingconfiguration.list
        - database.autoscalingpolicy.list
        - database.launchconfiguration.list
        - database.scalingprocesstype.list
        - database.scheuleaction.list
     
#### Storage
- ##### [Object Storage](https://api.ncloud-docs.com/docs/storage-objectstorage)
    - Scopes
        - https://api.ncloud-docs.com/docs/storage-objectstorage-listbuckets
        - https://api.ncloud-docs.com/docs/storage-objectstorage-listobjects
        - https://api.ncloud-docs.com/docs/storage-objectstorage-getbucketco

    - IAM
        - storage.bucket.list
        - storage.object.list
        - storage.bucketco.list
     
        - 
- ##### [Archive Storage](https://api.ncloud-docs.com/docs/storage-archivestorage)
    - Scopes
        - https://api.ncloud-docs.com/docs/storage-archivestorage-getaccount
        - https://api.ncloud-docs.com/docs/storage-archivestorage-getcontainer
  

    - IAM
        - storage.account.list
        - storage.container.list
        
      


#### Networking
- ##### [VPC](https://api.ncloud-docs.com/docs/networking-vpc)
    - Scopes
        - https://api.ncloud-docs.com/docs/networking-vpc-vpcmanagement-getvpclist
        - https://api.ncloud-docs.com/docs/networking-vpc-vpcmanagement-getvpcdetail
        - https://api.ncloud-docs.com/docs/networking-vpc-subnetmanagement-getsubnetlist
        - https://api.ncloud-docs.com/docs/networking-vpc-subnetmanagement-getsubnetdetail
        - https://api.ncloud-docs.com/docs/networking-vpc-networkacl-getnetworkacllist
        - https://api.ncloud-docs.com/docs/networking-vpc-networkacl-getnetworkacldetail
        - https://api.ncloud-docs.com/docs/networking-vpc-natgateway-getnatgatewayinstancelist
        - https://api.ncloud-docs.com/docs/networking-vpc-natgateway-getnatgatewayinstancedetail
        - https://api.ncloud-docs.com/docs/networking-vpc-vpcpeering-getvpcpeeringinstancelist
        - https://api.ncloud-docs.com/docs/networking-vpc-vpcpeering-getvpcpeeringinstancedetail
        - https://api.ncloud-docs.com/docs/networking-vpc-routetable-getroutetablelist
        - https://api.ncloud-docs.com/docs/networking-vpc-routetable-getroutetabledetail
        - https://api.ncloud-docs.com/docs/networking-vpc-routetable-getroutetablesubnetlist
     
    - IAM
        - networking.vpc.list
        - networking.vpcdetail.list
        - networking.subnet.list
        - networking.subnetdetail.list
        - networking.networkacl.list
        - networking.networkacldetail.list
        - networking.gatewayinstance.list
        - networking.gatewayinstancedetail.list
        - networking.peeringinstance.list
        - networking.peeringinstancedetail.list
        - networking.routetable.list
        - networking.routetabledetail.list
        - networking.routetablesubnet.list
        
     

     
#### Management
- ##### [Monitoring](https://api.ncloud-docs.com/docs/management-monitoring)
    - Scopes
  
        - https://api.ncloud-docs.com/docs/management-monitoring-getlistmetrics
     
    - IAM
        - management.metrics.list

        
     
     
#### Content Delivery
- ##### [CDN](https://api.ncloud-docs.com/docs/networking-cdn)
    - Scopes
        - https://api.ncloud-docs.com/docs/networking-cdn-getcdnplusinstancelist
        - https://api.ncloud-docs.com/docs/networking-cdn-getcdnpluspurgehistorylist
        - https://api.ncloud-docs.com/docs/networking-cdn-getglobalcdninstancelist
        - https://api.ncloud-docs.com/docs/networking-cdn-getglobalcdnpurgehistorylist

    - IAM
        - contentdelivery.cdnplusinstance.list
        - contentdelivery.cdnpluspurgehistory.list
        - contentdelivery.cdnglobalinstance.list
        - contentdelivery.cdnglobalpurgehistory.list
  




---

## Options

### Cloud Service Type : Specify what to collect

If cloud_service_types is added to the list elements in options, only the specified cloud service type is collected.
By default, if cloud_service_types is not specified in options, all services are collected.

The cloud_service_types items that can be specified are as follows.

<pre>
<code>
{
    "cloud_service_types": [
        'Compute',          
        'Database',     
        'Storage',       
        'Management',
        'Networking',
        'Content Delivery',

        
    ]
}
</code>
</pre>

## Ncloud Service Endpoint (in use)

### ObjectStorage
Naver Cloud Platform Object Storage provides the S3 API for storage management and use.
Version: Amazon S3 v2006-03-01


We use hundreds of endpoints because we collect information from a lots of regions and services.  

- ### Region list


|No.|Region   | Region name |Endpoint|
|-|---------|-------------|--------|
|1|한국  | kr-standard|https://kr.object.ncloudstorage.com|
|2|미국서부(New) |us-standard|https://us.object.ncloudstorage.com|
|3|싱가포르(New)|sg-standard|https://sg.object.ncloudstorage.com|
|4|일본(New)|jp-standard|https://jp.object.ncpstorage.com|
|5|독일(New)|de-standard|https://de.object.ncloudstorage.com|

### ArchiveStorage

- ### Region URL
Naver cloud platform Archive Storage provides the NSX Swift API for storage management and use.
Version: 2.15.1 (Pike)


|No.|Region   | Authentication URL |Service URL|
|-|---------|-------------|--------|
|1|한국  | https://kr.archive.ncloudstorage.com:5000|https://kr.archive.ncloudstorage.com|
|2|한국 |https://archivestorage.apigw.ntruss.com/swift/v1/|https://archivestorage.apigw.ntruss.com/swift/v1/|


---
## [Release note](RELEASE.md)
