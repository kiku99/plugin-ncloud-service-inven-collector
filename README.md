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
|5| Vpc            |networking|
|6| Monitoring     |management|
|7| CDN            |content delivery|



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
  
    * [Networking](#networking)
        * [Vpc](#vpc)
  
    * [Management](#management)
        * [Monitoring](#monitoring)
  
    * [Content Delivery](#content-delivery)
        * [Cdn](#cdn)
<br>

## Authentication Overview
Registered service account on SpaceONE must have certain permissions to collect cloud service data
Please, set authentication privilege for followings:

#### Compute

- ##### [Server](https://api.ncloud-docs.com/docs/compute-server)
    - Scopes
        - https://api.ncloud-docs.com/docs/compute-server-getserverinstancelist
        - https://api.ncloud-docs.com/docs/compute-server-getblockstorageinstancelist
        - https://api.ncloud-docs.com/docs/compute-server-getloginkeylist

- ##### [Autoscaling](https://api.ncloud-docs.com/docs/compute-autoscaling)
    - Scopes
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getadjustmenttypelist
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getautoscalingactivityloglist
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getautoscalingconfigurationloglist
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getautoscalingpolicylist
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getlaunchconfigurationlist
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getscalingprocesstypelist
        - https://api.ncloud-docs.com/docs/compute-autoscaling-getscheduledactionlist
     

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
     
#### Storage
- ##### [Object Storage](https://api.ncloud-docs.com/docs/storage-objectstorage)
    - Scopes
        - https://api.ncloud-docs.com/docs/storage-objectstorage-listbuckets
        - https://api.ncloud-docs.com/docs/storage-objectstorage-listobjects
        - https://api.ncloud-docs.com/docs/storage-objectstorage-getbucketco


#### Networking
- ##### [Vpc](https://api.ncloud-docs.com/docs/networking-vpc)
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
     

     
#### Management
- ##### [Monitoring](https://api.ncloud-docs.com/docs/management-monitoring)
    - Scopes
        - https://api.ncloud-docs.com/docs/management-monitoring-getmetricstatisticlist
        - https://api.ncloud-docs.com/docs/management-monitoring-getlistmetrics
        
     
     
#### Content Delivery
- ##### [Cdn](https://api.ncloud-docs.com/docs/networking-cdn)
    - Scopes
        - https://api.ncloud-docs.com/docs/networking-cdn-getcdnplusinstancelist
        - https://api.ncloud-docs.com/docs/networking-cdn-getcdnpluspurgehistorylist
        - https://api.ncloud-docs.com/docs/networking-cdn-getglobalcdninstancelist
        - https://api.ncloud-docs.com/docs/networking-cdn-getglobalcdnpurgehistorylist
          
  




---

## Options

TBD
