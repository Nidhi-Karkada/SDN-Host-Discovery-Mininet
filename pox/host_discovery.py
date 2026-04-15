from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# -------------------------------
# HOST DATABASE (MAC → details)
# -------------------------------
hosts = {}

# -------------------------------
# BLOCK RULES (edit for demo)
# -------------------------------
blocked_pairs = [
    ("10.0.0.1", "10.0.0.2"),  # h1 → h2 blocked
]

# -------------------------------
# PRINT HOST TABLE
# -------------------------------
def print_hosts():
    log.info("------ HOST TABLE ------")
    for mac, info in hosts.items():
        log.info("MAC=%s IP=%s Switch=%s Port=%s",
                 mac, info["ip"], info["dpid"], info["port"])
    log.info("------------------------")


# -------------------------------
# SWITCH CONNECT EVENT
# -------------------------------
def _handle_ConnectionUp(event):
    log.info("[SWITCH CONNECTED] DPID=%s", event.dpid)


# -------------------------------
# PACKET IN HANDLER (CORE LOGIC)
# -------------------------------
def _handle_PacketIn(event):
    packet = event.parsed

    if not packet.parsed:
        return

    ip_packet = packet.find('ipv4')

    # -------------------------------
    # HOST DISCOVERY + DATABASE
    # -------------------------------
    if packet.src not in hosts:
        hosts[packet.src] = {
            "ip": str(ip_packet.srcip) if ip_packet else "Unknown",
            "dpid": event.dpid,
            "port": event.port
        }

        log.info("[NEW HOST] MAC=%s IP=%s Switch=%s Port=%s",
                 packet.src,
                 hosts[packet.src]["ip"],
                 event.dpid,
                 event.port)

        print_hosts()

    # -------------------------------
    # BLOCKING LOGIC (MATCH-ACTION)
    # -------------------------------
    if ip_packet:
        src = str(ip_packet.srcip)
        dst = str(ip_packet.dstip)

        if (src, dst) in blocked_pairs:
            log.info("[BLOCKED] %s -> %s", src, dst)

            # Install DROP rule
            msg = of.ofp_flow_mod()
            msg.match.dl_type = 0x0800  # IPv4
            msg.match.nw_src = ip_packet.srcip
            msg.match.nw_dst = ip_packet.dstip

            event.connection.send(msg)
            return

    # -------------------------------
    # DEFAULT FORWARDING (HUB)
    # -------------------------------
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)


# -------------------------------
# LAUNCH FUNCTION
# -------------------------------
def launch():
    log.info("Starting SDN Host Discovery + Control App...")

    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
