terraform {

  required_version = ">= 1.2.0"

  required_providers {
    harvester = {
      source  = "harvester/harvester"
      version = "0.6.4"
    }

    random = {
      source = "hashicorp/random"
      version = "3.6.1"
    }

    tls = {
      source = "hashicorp/tls"
      version = ">= 4.0.4"


    }
  }
  
}
