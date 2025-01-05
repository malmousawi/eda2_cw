output "host_vm_ips" {
  value = harvester_virtualmachine.host[*].network_interface[0].ip_address
}

output "host_vm_ids" {
  value = harvester_virtualmachine.host[*].id
}

output "worker_vm_ips" {
  value = harvester_virtualmachine.worker[*].network_interface[0].ip_address
}

output "worker_vm_ids" {
  value = harvester_virtualmachine.worker[*].id
}

output "storage_vm_ips" {
  value = harvester_virtualmachine.storage[*].network_interface[0].ip_address
}

output "storage_vm_ids" {
  value = harvester_virtualmachine.storage[*].id
}

