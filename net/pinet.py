import socket
import json
import random
import time
import logging as log
from typing import Union, List, Dict
from threading import Thread
from .pineterror import PiNetError

# Constants
NETWORK_TIMEOUT = 0.1


class PiNet:
    """ PiNet is an asynchronous socket wrapper to facilitate communications
    between different Raspberry Pi computers (and indeed other computers).
    The class is intended to facilitate easy communication over LAN using
    JSON encoding. Furthermore, all networking operations are designed to run
    in separate threads to that of the dispatching main program, preventing
    lockups and allowing time critical execution to continue unaffected.
    """

    def __init__(self, is_server: bool, address: (str, int)) -> None:
        """ Constructs a new instance of PiNet.

        isServer - A boolean value indicating if the new PiNet object is to be a
            server (True) or a client (False).
        address - The network address to bind the connection to.
        port - The network port the PiNet will create connections with. Must be
            between 0 and 65535 inclusive.

        Raises PiNetError "Invalid port." when the provided port is not within
            the	range 0 to 65535 inclusive.
        """
        socket.setdefaulttimeout(NETWORK_TIMEOUT)
        if not 0 <= address[1] <= 65535:
            raise PiNetError("Invalid port.")
        self.__address = address
        self.__isServer = is_server
        self.__responses = {}
        self.__requests = []
        self.__messages = []
        self.__conn = {"thread": None, "conn": None, "host": None,
                       "isRunning": False}
        self.__clients = {}

    def start(self) -> None:
        """ Starts the process by which the PiNet instance will seek a network
        connection with other computers.

        Raises PiNetError 'Unable to connect to server.' if a connection with
            the	specified server cannot be established.
        Raises PiNetError 'Socket connection already running.' if the socket is
            already connected.
        """
        if self.__conn["thread"] is None:
            if self.__isServer:
                self.__conn["isRunning"] = True
                self.__conn["thread"] = Thread(target =self.__accept_clients)
                self.__conn["conn"] = socket.socket()
                self.__conn["conn"].bind(self.__address)
                self.__conn["thread"].start()
                self.__conn["conn"].listen()
                log.info("Server listening for clients on "
                         "{0}.".format(self.__address))
            else:
                try:
                    self.__conn["conn"] = socket.socket()
                    self.__conn["conn"].connect(self.__address)
                except:  # Unable to determine the relevant exception type
                    log.error("Unable to connect to server at "
                              "{0}.".format(self.__address))
                    raise PiNetError("Unable to connect to server.")
                else:
                    self.__conn["isRunning"] = True
                    self.__conn["thread"] = Thread(target=self.__tend_server)
                    self.__conn["thread"].start()
                    log.info("Client connected to server at "
                             "{0}.".format(self.__address))
        else:
            log.error("Socket connection already running")
            raise PiNetError("Socket connection already running.")

    def is_running(self) -> bool:
        """ Returns a boolean indicating whether or not the connection is
        active.
        """
        return self.__conn["isRunning"]

    def set_address(self, address: (str, int)) -> None:
        """ Updates the address of the connection. Can only be called if
        isRunning() is False.

        Raises PiNetError 'Cannot change the connection address while the
            connection is active' if called when isRunning() is True.
        """
        if self.__conn["isRunning"]:
            log.warning("Cannot change the connection address while the "
                        "connection is active")
            raise PiNetError("Cannot change the connection address while the "
                             "connection is active")
        else:
            self.__address = address

    def send_request(self, request: Dict[str, any], target="") -> int:
        """ Sends a request to a peer (who must be specified if called by a
        server instance). Returns a responseKey integer  to retrieve the JSON
        payload returned by the peer with getResponse(). The response payload
        will be a dict with the format {"requestKey": (int), "response":
        (any)}.

        request - A dictionary of the format {"type": ["action"|"get"|"set"],
            "name": ["name"], ["args": []], ["value": any]}
        target - If the caller is a server, it is necessary to specify which
            client the outgoing request is to be sent to. An exception will be
            raised if target is its default value in this case.

        Raises PiNetError 'Invalid request' if the request does not follow the
            specified format.
        Raises PiNetError 'Target not specified for the request' when the target
            parameter is not given when called by a server instance of PiNet.
        Raises PiNetError 'Specified target is not available.' when the client
            peer targeted by the operation is not connected.
        """
        if type(request) != dict or "type" not in request or "name" not in request:
            log.error("Invalid request.")
            raise PiNetError("Invalid request.")
        requestKey = self.__register_response()
        request.update({"requestKey", requestKey})
        requestPayload = json.dumps(request, separators=(',', ':'))
        if self.__isServer:
            target = str(target)
            if target != "":
                if target in self.__clients and self.__clients[target]["isRunning"]:
                    st = Thread(target=self.__send,
                                args=(self.__clients[target], requestPayload))
                    st.start()
                else:
                    log.error("Specified target is not available.")
                    raise PiNetError("Specified target is not available.")
            else:
                log.error("Target not specified for the request.")
                raise PiNetError("Target not specified for the request.")
        else:
            st = Thread(target=self.__send,
                        args=(self.__conn, requestPayload))
            st.start()
        return requestKey

    def send_msg(self, msg: str, target="") -> None:
        """ Sends a message to a peer. Unlike sendRequest(), a response from the
         peer is not expected.

        msg - A string containing the message to be sent.
        target - If the caller is a server, it is necessary to specify which
            client the outgoing message is to be sent to. An exception will be
            raised if target is its default value in this case.

        Raises PiNetError 'Target not specified for the message' when the target
            parameter is not given when called by a server instance of PiNet.
        Raises PiNetError 'Specified target is not available.' when the client
            peer targeted by the operation is not connected.
        """
        msgPayload = {"type": "msg", "msg": msg}
        msgPayload = json.dumps(msgPayload , separators=(',', ':'))
        if self.__isServer:
            target = str(target)
            if target != "":
                if target in self.__clients and self.__clients[target]["isRunning"]:
                    st = Thread(target=self.__send,
                                args=(self.__clients[target], msgPayload))
                    st.start()
                else:
                    log.error("Specified target is not available.")
                    raise PiNetError("Specified target is not available.")
            else:
                log.error("Target not specified for the message.")
                raise PiNetError("Target not specified for the message.")
        else:
            st = Thread(target=self.__send, args=(self.__conn, msgPayload))
            st.start()

    def get_msg(self) -> Union[str, List[str], None]:
        """ Returns the most recent message received by a peer as a string. If
        there are no messages, None is	returned.
        """
        if len(self.__messages) > 0:
            return self.__messages.pop(0)
        else:
            return None

    def get_response(self, key: int) -> Union[dict, None]:
        """ Called by a thread after dispatching a request to a peer to obtain
        the returned JSON response.

        key - The responseKey integer returned by the request dispatching
            function.
        """
        if key in self.__responses and self.__responses[key] is None:
            return self.__responses.pop(key)
        else:
            return None

    def send_response(self, response_key: int, value: any, peer: dict) -> None:
        """ Sends a response to a request made by a peer.

        responseKey - The responseKey integer provided with the request.
        value - The value to be returned as a response to the request.
        peer - The connection-specific peer identifier provided as a dictionary
            as part of the request.
        """
        response = {"responseKey": response_key, "response": value}
        payload = json.dumps(response, separators=(',', ':'))
        st = Thread(target=self.__send, args=(peer, payload))
        st.start()

    def get_request(self) -> Union[dict, None]:
        """ Returns the most recent request payload as a dictionary. If no
        requests exist then None is returned.
        """
        if len(self.__requests) > 0:
            return self.__requests.pop(0)
        else:
            return None

    def stop(self) -> None:
        """ Correctly terminates a connection with peers as soon as possible
        and kills all open threads.
        """
        if self.__conn["isRunning"]:
            closePayload = json.dumps("closing", separators=(',', ':')).encode()
            self.__conn["isRunning"] = False
            self.__conn["thread"].join()
            if self.__isServer:
                log.info("Closing client listener at "
                         "{0}.".format(self.__address))
                for host, client in self.__clients.items():
                    client["isRunning"] = False
                    client["thread"].join()
                    try:
                        client["conn"].sendall(closePayload)
                    except:  # Unable to determine the relevant exception type
                        pass
                    finally:
                        time.sleep(NETWORK_TIMEOUT)
                    client["conn"].close()
                    log.info("Closing client connection at "
                             "{0}.".format(client["host"]))
            else:
                log.info("Closing server connection at "
                         "{0}.".format(self.__address))
                try:
                    self.__conn["conn"].sendall(closePayload)
                except:  # Unable to determine the relevant exception type
                    pass
                finally:
                    time.sleep(NETWORK_TIMEOUT)
            self.__conn["conn"].close()
            self.__responses = {}
            self.__messages	= []

    def get_connected(self) -> List[str]:
        """ Returns a list of all the connected client's host names. The
        names are used to target peers when performing operations as a server
        instance. Peers reflected in this list are available to data
        transmission or reception.

        Raises PiNetError "Invalid operation for clients." when called from a
            client instance.
        """
        if self.__isServer:
            return list(self.__clients.keys())
        else:
            log.warning("Clients should not call getConnected().")
            raise PiNetError("Invalid operation for clients.")

    def __register_response(self) -> int:
        """ Called by a method dispatching a request to obtain a responseKey
        so that any data returned in a response may be obtained after with
        getResponse().

        Raises PiNetError "Fatal, maximum number of pending responses exceeded."
            when there are 256 responses already registered and waiting
            collection.	Intentionally left uncaught as under correct
            implementation and normal operation should never occur.
        """
        if len(self.__responses) == 256:
            log.critical("Fatal, maximum number of pending responses exceeded.")
            raise PiNetError("Fatal, maximum number of pending responses "
                             "exceeded.")
        key = random.randint(0, 255)
        while key in self.__responses:
            key = random.randint(0, 255)
        self.__responses[key] = ""
        return key

    def __send(self, peer: dict, payload: str) -> None:
        """ Called asynchronously to send messages to a specified peer.

        peer - The connection-specification dictionary of the peer the message
            should be sent to.
            payload - A string containing the message to be sent.
        """
        try:
            peer["conn"].sendall(payload.encode())
        except:
            peer["isRunning"] = False
            peer["conn"].close()
            peer["thread"].join()
            if self.__isServer:
                for host, client in self.__clients.items():
                    if client == peer:
                        log.error("Failed to send message to client at {0}, "
                                  "closing socket.".format(peer["host"]))
                        self.__clients.pop(host)
                        break
            else:
                log.error("Failed to send message to server at {0}, "
                          "closing socket.".format(self.__address))
                self.__conn["thread"] = None

    def __accept_clients(self) -> None:
        """ Called asynchronously in server instances to constantly listen for
        remote clients attempting to connect.
        """
        while self.__conn["isRunning"]:
            try:
                conn, host = self.__conn["conn"].accept()
            except:  # Unable to determine the relevant exception type
                # This will be caught continually
                pass
            else:
                self.__clients[str(host[1])] = {"thread": None, "conn": conn,
                                                "isRunning": True, "host": host}
                thread = Thread(target=self.__tend_client,
                                args=[self.__clients[str(host[1])]])
                self.__clients[str(host[1])]["thread"] = thread
                thread.start()
                log.info("Client connected from {0}.".format(host))

    def __handle_msg(self, peer: dict) -> None:
        """ Called by an asynchronous thread servicing a connection to receive
        messaged from its peer and address them accordingly.

        peer - The connection-specification dictionary for the client to be
            serviced.
        """
        inPayload = self.__recv_payload(peer)
        if inPayload == "":
            return
        elif inPayload == "closing":
            if self.__isServer:
                peer["isRunning"] = False
                peer["conn"].close()
                log.info("Client connection closed by peer from "
                         "{0}.".format(peer["host"]))
                self.__clients.pop(str(peer["host"][1]))
            else:
                log.info("Connection closed by server from "
                         "{0}".format(self.__address))
                self.__conn["isRunning"] = False
            return
        elif "responseKey" in inPayload:
            if inPayload["responseKey"] in self.__responses:
                self.__responses[inPayload["responseKey"]] = inPayload
        elif "type" in inPayload:
            if inPayload["type"] == "msg":
                self.__messages.append(inPayload["msg"])
            elif inPayload["type"] == "action" or inPayload["type"] == "data":
                inPayload.update({"peer": peer})
                self.__requests.append(inPayload)

    def __tend_client(self, peer: dict) -> None:
        """ Called asynchronously in server instances to service a connection
        opened with a client.

        peer - The connection-specification dictionary for the client to be
            serviced.
        """
        while peer["isRunning"]:
            self.__handle_msg(peer)

    def __tend_server(self) -> None:
        """ Called asynchronously in client instances to service a connection
        opened with a server.

        peer - The connection-specification dictionary for the client to be
            serviced.
        """
        while self.__conn["isRunning"]:
            self.__handle_msg(self.__conn)

    def __recv_payload(self, peer: dict) -> dict:
        """ Called by an asynchronous thread to receive messages from a
        specified peer.

        peer - The connection-specification dictionary of the peer the message
            should be received from.
        """
        request = ""
        while True:
            data = None
            try:
                data = peer["conn"].recv(1024)
            except:  # Unable to determine the relevant exception type
                pass
            if data is None:
                if len(request) > 0:
                    return json.loads(request)
                else:
                    return {}
            else:
                request = request + data.decode()
