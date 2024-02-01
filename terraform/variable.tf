#location name
variable "location" {
  type        = string
  description = "Resources location in Azure"
}
#datalake name
variable "datalake_name"{
    type        = string
    description = "Datalake name in Azure"
}
#database server name
variable "server_name"{
    type        = string
    description = "Database server name in Azure"
}
#database_name
variable "database_name"{
    type        = string
    description = "Database name in Azure"
}

/* #Kubernetes-cluster name
variable "cluster_name" {
  type        = string
  description = "AKS name in Azure"
}
#kubernetes-version number
variable "kubernetes_version" {
  type        = string
  description = "Kubernetes version"
}
#node count
variable "system_node_count" {
  type        = number
  description = "Number of AKS worker nodes"
}
#Acr name
variable "acr_name" {
  type        = string
  description = "ACR name"
} */