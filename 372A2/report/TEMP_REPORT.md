 

Introduction 

Goal of the assignment 

This assignment creates and tests two protocols that are necessary for ensuring reliable transport of data Stop-and-Wait and Go-Back-N (GBN). Both of these protocols have been implemented based on the principles of User Datagram Protocol (UDP), which does not guarantee any delivery of packets, so the current project uses all the techniques required for ensuring the reliability of the process of data transport, such as sequence numbers, ACKs, timers, and retransmission. 

Background 

UDP 

UDP is a connectionless, unreliable transport layer protocol. It sends datagrams without setting up a connection, without guaranteeing delivery, ordering, or duplication, and without managing flows. This means that UDP is quicker and more efficient than TCP; however, it also implies that any application that relies on reliable delivery of messages by UDP needs to manage that reliability at the application level – which is the objective of this project. 

General principal of reliability 

Transfer of reliable data across an unreliable network can be done by using four fundamental building blocks: (1) sequence number, which allows the receiver to keep track of each and every packet and also find out any duplicate or lost packet; (2) acknowledgment, which keeps the sender informed about the receipt of particular packets; (3) timers, which help the sender to know that whether his packets (or their acknowledgement) have been lost or not; and (4) retransmission of lost packets. 

Stop-and-Wait Protocol 

The simplest and most effective approach to transfer data is the use of a stop-and-wait approach. The sender transmits a single packet and then waits until he receives an acknowledgement before sending another packet. In case the acknowledgement is not received within the time limit, the sender transmits the same packet again. While this makes the process accurate, the channel remains idle until an acknowledgment is received. 

Go-Back-N Protocol 

Go-Back-N expands upon Stop-and-Wait by sending multiple packets before acknowledging them through a sliding window of size N. The sender keeps track of the oldest outstanding packet (base) and the next sequence number (nextseqnum). Additionally, there is a single timer maintained for the oldest packet sent. The receiver accepts packets only in order and sends cumulative ACKs. Out of order packets, if any, get discarded. In case of timeouts, all the packets in the window starting from the base are retransmitted. This pipelining makes Go-Back-N more efficient than Stop-and-Wait but involves retransmission of packets that might have been successfully transmitted already. 

Design 

Packet format 

Stop-and-Wait design 

Sender logic 

Divides the file or generated content into fixed-size packets before sending. 
Sends a control packet to tell the receiver of a new file transfer starting 
Sends one DATA packet, sets a timer, then waits for an ACK before sending the next packet 
Retransmits an unacknowledged packet after a timeout 
After acknowledging the last packet, send a completion/control packet to signify the conclusion of the transfer. 
Receiver logic 

Checks incoming packets against expected sequence numbers 
Sends an acknowledgement (ACK) for each correctly received, in-order packet 
Creates a new file upon getting the "start of transfer" control packet, writes payload data for DATA packets, and closes upon receiving the "completion" control packet 
Re-ACKs duplicate or out-of-order packets, but ignores them otherwise 
*add specific timeout value and say why we chose that 

Go-back-N Design 

Sender logic 

Contains three state variables: base (the oldest unacknowledged sequence number), nextseqnum (the next sequence number to assign), and window size (the maximum number of unacknowledged packets allowed) 
Sends packets constantly if nextseqnum is inside base + window size, without waiting for individual ACKs 
Runs a timer for the oldest unacknowledged packet (at base) 
Accepts incoming ACKs as cumulative: an ACK for sequence number k validates all packets up to and including k, and advances the base correspondingly 
On timeout, retransmit all packets in the window, from base to nextseqnum - 1 
Receiver logic 

Retains a single predicted sequence number 
Accepts packets only if their sequence number matches the expected value; otherwise, they are discarded 
After receiving a packet, increment the expected sequence number and send a cumulative ACK for the highest in-order packet received to date 
*add window size and reasoning behind that 

Packet loss format 

The figure below shows how each protocol detects and recovers from a lost packet (or lost ACK) using timeout-driven retransmission. 

*add diagram 

 

Experimental results 

Each cell below is the average of at least five independent test runs for the file size and loss rate combination specified in the assignment. All times are measured in seconds. 

Average Stop-n-Wait 

Table.1 Average Stop-and-Wait Transfer Time (average of at least 5 tests per file size per loss rate)  

Loss rate 
10K 
50K 
100K 
500K 
1M 
5M 
10M 
50M 
100M 
0% 
0.001 
0.002 
0.003 
0.009 
0.016 
0.045 
0.076 
0.306 
0.596 
10% 
0.008 
0.003 
0.048 
0.240 
0.488 
2.299 
4.618 
23.11 
45.65 
20% 
0.021 
0.109 
0.168 
0.523 
0.846 
5.259 
9.974 
50.96 
103.2 
30% 
0.065 
0.134 
0.241 
0.854 
1.822 
8.646 
16.95 
84.91 
171.6 
 

 

Average Go-Back-N 

Table.2 Average GBN transfer Time (average of at least 5 tests per file size per loss rate) 

Loss rate 
10K 
50K 
100K 
500K 
1M 
5M 
10M 
50M 
100M 
0% 
0.001 
0.003 
0.003 
0.006 
0.010 
0.031 
0.055 
0.230 
0.442 
10% 
0.032 
0.342 
0.071 
0.200 
0.416 
2.304 
4.507 
22.06 
44.94 
20% 
0.063 
0.033 
0.151 
0.416 
1.086 
4.981 
9.945 
49.04 
97.02 
30% 
0.045 
0.120 
0.232 
1.086 
1.814 
8.688 
17.11 
85.86 
174.6 
 

 

Metrics 

In addition to transfer time, the following metrics were measured for each file size / loss rate combination (averaged over 5 runs), as specified by the assignment: average throughput (bytes/second) and average number of retransmissions. 

*add (1) Average Throughput (bytes/sec) for both protocols, and (2) Average Number of Retransmissions for both protocols 

Graphics 

The charts below show how transfer time and throughput vary with file size and loss rate for both protocols. 

*add charts 

Analysis 

Why is GBN always faster than Stop-n-wait? 

GBN is faster because it keeps the network busy instead of remaining idle after every packet. Stop-n-Wait transmits one packet and stays idle until its ACK arrives creating a round-trip delay for every packet. GBN uses a sliding window, that allows the user to send multiple packets continuously without waiting for individual acknowledgement. 

Impact of increasing packet loss 

 

Trade-offs between simplicity and efficiency 

Stop-and-Wait is straightforward to build and understand: there is never more than one unacknowledged packet in flight, thus there is no need to manage a window, deal with out-of-order arrivals, or track multiple timers. This simplicity comes at the cost of low channel utilization: the link is idle for the majority of each round-trip period. Go-Back-N is more sophisticated, but it provides substantially higher performance on networks with non-trivial round-trip time since it combines transmission and acknowledgment wait time. 

When Stop-n-wait might still be useful 

For small and/or rare transfer requests, window handling can prove more expensive than the pipelining gain 
Small memory devices will have difficulties buffering multiple unacknowledged messages 
Low-complexity networks where efficiency is sacrificed in favor of simplicity and predictability 
GBN's pipelining advantage may get outweighed by window-wide retransmissions on loss-prone or congested links, as illustrated in this assignment 
Conclusion 

This project demonstrates how reliable data transfer can be implemented over UDP using Stop-and-Wait and Go-Back-N protocols. Experimental results show that ...  

In order to increase overall throughput, we can consider the use of Selective Repeat protocol, which means only the missing packet will be sent back while not all packets within a window are resent like in the Go-Back-N protocol, setting the timeout according to the actual round trip time, and changing the window size according to the loss rate.	 

 