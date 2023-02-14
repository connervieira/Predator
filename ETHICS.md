# Ethics

As with all V0LT projects, ethics is a core element of Predator's development. This document explains a lot of the ethical points that Predator adheres to.


## Transparency

As you likely already know, Predator (and all of its dependencies) are completely open source and freely auditable. When it comes to Predator itself, anyone with the appropriate technical knowledge is free to audit the code the powers it.


## ALPR

The practice of automated license plate recognition (ALPR) is a very delicate subject. On one hand, ALPR can help find dangerous criminals and missing children. However, well over 99% of the license plates recorded by public ALPR systems are used to track the locations of innocent people, without warrants or other supervising measures.

### Alerts

Predator provides the ability to alert the user when it detects a license plate in an alert hotlist. These alerts can be used by users to receive alerts when they pass family members on the road, drive by a famous car, or any other situation they can think of. However, this feature can also be used in more serious situations, like AMBER alert plate detection.

For sake of conveinence and unity, V0LT occasionally provides optional network based license plate alert hotlists to aid users who want to help their communities catch dangerous criminals. That being said, V0LT has extremely strict policies on what license plates are posted to this list.

Alerts may be published for the following situations:

1. A vehicle was recently stolen.
2. A violent criminal was last seen in a particular vehicle.
3. An AMBER alert published by law enforcement contained a license plate.

In order to protect privacy, alerts are not published for the following situations:

1. Vehicles involved in non-violent crimes.
2. Vehicles that witnessed a crime.
3. Vehicles that may have been involved in violent crimes, but not recently.
4. Missing person cases without concrete evidence to suggest abduction or other violence.


## Privacy

Traditional ALPR platforms are designed for mass data collection and analysis. Conversely, Predator is designed to be a completely stand-alone, offline platform. Predator is not designed to track vehicles, and doesn't submit any data to a central server. Individual Predator users are responsible for protecting the privacy and integrity of the data the collect. Predator itself doesn't transmit any personal information, unless explicity configured to by the user.


## Control

Predator is designed in such a way that the user has full control over the entire system. Predator's configuration makes it easy to turn various features on and off to better fit each situation's use case and privacy concerns.
