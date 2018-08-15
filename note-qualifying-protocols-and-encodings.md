# Qualifying Protocols and Encodings

The explicit goal of the CloudEvents effort, as expressed in the specification, is 
"describing event data in a common way" and "to define interoperability of event 
systems that allow services to produce or consume events, where the producer and 
consumer can be developed and deployed independently".

The foundation for such interoperability are open data formats and open protocols,
with CloudEvents aiming to provide such an open data format and projections of 
its data format onto commonly used protocols and with commonly used encodings.

While each software or service product and project can obviously make its own 
choices about which form of communication it prefers, its unquestionable that 
a proprietary protocol that is private to such a product or project does not 
further the goal of broad interoperability across producers and consumers of 
events.

Especially in the area of messaging and eventing, the industry has made significant 
progress in the last decade in developing a robust and broadly supported protocol 
foundation, like HTTP 1.1 and HTTP/2 as well as WebSockets or events on the web, 
or MQTT and AMQP for connection-oriented messaging and telemetry transfers.

Some widely used protocols have become de-facto standards emerging out of strong
ecosystems of top-level multi-company consortia projects, such as Apache Kafka, 
and largely in parallel to the evolution of the aforementioned standards stacks.

The CloudEvents effort shall not become a vehicle to even implicitly endorse 
or promote project- or product-proprietary protocols, because that would be 
counterproductive towards CloudEvents' original goals. 

For a protocol or encoding to qualify for a core CloudEvents event format or 
protocol binding, it must belong to either one of the following categories:

- The protocol has a formal status as a standard with a widely-recognized 
  multi-vendor protocol standardization body (e.g. W3C, IETF, OASIS, ISO)
- The protocol has a "de-facto standard" status for its ecosystem category,
  which means it is used so widely that it is considered a standard for a
  given application. Practically, we would like to see at least one open
  source implementation and at least a dozen independent vendors using it
  in their products/services.

Aside from formal status, a key criterion for whether a protocol or encoding shall 
qualify for a core CloudEvents event format or transport binding is whether the 
working group agrees that the specification will be of sustained practical benefit 
for any party that is unrelated to the product or project from which the protocol 
or encoding emerged. A base requirement for this is that the protocol or encoding 
is defined in a fashion that allows alternate implementations independent of the 
product or project's code.

All other protocol and encoding formats for CloudEvents are welcome to be included
in a list pointing to the CloudEvents binding information in the respective 
project's own public repository or site.
