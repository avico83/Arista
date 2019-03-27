# Arista Monitoring Scripts:

The following scripts runs along with the schedule command.
While configuring the schedule command you can run scripts, and send variables to the script.

##### Schedule Arista CLI Command:

    schedule tracking_[route.name] now interval 2 timeout 1 max-log-files 30 logging verbose command bash sudo ip netns     exec ns-MGMT python /mnt/flash/static_route_tracking.py [route.destination] [route.next_hop] [route.name]

##### Monitor Arista CLI Command:
This pulls the the packect loss/latency via API

    monitor connectivity
    host [remote_device_name]
    ip [remote_device_name]
    no shutdown
