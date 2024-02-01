The aim of this project is to capture knowledge about building (dockerized) pipelines on Kubernetes.

The scope of the project is to build everything as Infrastructure as code. Right from deploying resource on azure using terraform to extracting data from API's and using dbt to do data manipulations. 

Scope:
Infrastructure-as-code elements (dev and prod)( using Terraform):
1. Create a resource group 
2. Create a Kubernetes cluster 
3. Create a data lake 
4. Create a database 

Kubernetes:
Have production and development separated by namespace

Docker (the pipeline):
- Pull from an API 
- Use retry on the API call using tenacity
- Store the data raw in the data lake
- Land data in a transformation layer (STAGING)
- Land data in a delta layer (DELTA)
- Land data in curated layer
- Store pipeline status during the pipeline run (at start and end)
When the pipeline fails during one of the stages, make the next run start where the pipeline failed (or a sensible place to retry the pipeline)

Kubernetes settings of the pod:
Make it retry 3x on failure
Schedule a run 2x a day (testing this might be the only reason to leave the cluster on during this POC when not developing for cost reasons)

Costs (minimal):
- Turn everything off when not developing or testing to minimize the costs
- Create the smallest possible AKS cluster (2 nodes I believe?)
- Database basic DTU (smallest possible)
- You can set a resourcing limit to your Resource group
