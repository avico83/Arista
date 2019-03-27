# Arista Monitoring Scripts:

The following scripts runs along with the schedule command.
While configuring the schedule command you can run scripts, and send variables to the script.

### Example of how to run the script from Arista cli:

schedule tracking_{{ route.name }} now interval 2 timeout 1 max-log-files 30 logging verbose command bash sudo ip netns exec ns-MGMT python /mnt/flash/RouteTrack.py {{ route.destination }} {{ route.next_hop }} {{ route.name }}

### Peer Status script run as follows:
This pulls the the packect loss/latency via API

monitor connectivity
host {{ remote_device_name }}
ip {{ remote_device_name }}
no shutdown
