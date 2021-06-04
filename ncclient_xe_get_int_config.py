import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom


def main():
    """
    Main method that prints netconf capabilities of device.
    """

    parser = ArgumentParser(description='Select options.')
    # Input parameters
    parser.add_argument('--host', type=str, required=True,
                        help="The device IP or DN")
    parser.add_argument('-u', '--username', type=str, default='cisco',
                        help="Go on, guess!")
    parser.add_argument('-p', '--password', type=str, default='cisco',
                        help="Yep, this one too! ;-)")
    parser.add_argument('--port', type=int, default=830,
                        help="Specify this if you want a non-default port")
    args = parser.parse_args()

    # Device dictionary that provides key/value connection information
    device = {"ip": args.host, "port": args.port, "username": args.username, "password": args.password, "platform": "csr",}

    # ncclient manager instantiation for csr
    with manager.connect(host=device['ip'], port=device['port'], username=device['username'],
                         password=device['password'], hostkey_verify=False,
                         device_params={'name': device['platform']},
                         look_for_keys=False, allow_agent=False) as m:

        # Filter using top-level container namespace and node matching
        int_filter = '''
                    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        <interface>
                            <name>GigabitEthernet1</name>
                        </interface>
                    </interfaces>
                    '''

        # get-config RPC against the running datastore using a subtree filter
        reply = xml.dom.minidom.parseString( str (m.get_config('running', filter=('subtree', int_filter))))

        # Print RPC reply
        #print(reply)
        print(reply.toprettyxml( indent = "  " ))


if __name__ == '__main__':
    main()
