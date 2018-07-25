#!/usr/bin/env python

import asyncio
import config as cfg
import sys

class EscapeRoom():

    def __init__(self):
        pass

    def toggleLight(self, device):
        ret = self._request(f'toggle {device} builtin_led')
        if ret not in ['on', 'off']:
            print('Failed to toggle built-in led ')
        return ret

        
    def _request(self, msg):
        loop = asyncio.get_event_loop()
        ret = loop.run_until_complete(self._async_request(msg))
        loop.close()
        return ret

    async def _async_request(self, msg): # todo: add timeout
        reader, writer = await asyncio.open_connection(cfg.host, cfg.port)
        msg = msg.strip() + '\n'
        writer.write(msg.encode())
        data = await reader.readline()
        writer.close()
        return data.decode().strip()

    
if __name__ == '__main__':

    room = EscapeRoom()

    if len(sys.argv) < 2:
        print('Please specifie a request.')
        sys.exit(1) 

    request = ' '.join(sys.argv[1:])
    print(f'Sending: {repr(request)}')
    print('\t-> ' + room._request(request))

