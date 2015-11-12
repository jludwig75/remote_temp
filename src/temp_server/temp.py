def onRequestComplete(request, status):
    pass

def main():
    si = create_storage_inerface(skunk_ulator/ram_drive)
    
    ftl_startup()
    
    bd = si.create_block_device()
    #bd.set_completion_callback(onRequestComplete)
    
    buffer = host_data_buffer(size)
    set_pattern(buffer)
    
    reqs = []
    req = block_device_request(operation, offset, length, buffer)
    bd.handle_request(req)
    reqs.append(req)
    
    while bd.requests_in_flight() > 0:
        ftl_advance()
        si.process_io()
    
    for req in reqs:
        #check req
        pass
    
    ftl_cleanup()