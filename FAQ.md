# Frequently Asked Questions

This document contains a series of questions you may have concerning Predator.


**What exactly is Predator?**

Predator is a camera utility designed primarily to be installed in a vehicle. It is focused on license plate reading and object recognition, although it works as a fully featured traditional dash-cam as well.


**How do I install Predator?**

For installation and setup instructions, check the [DOCUMENTATION.md](DOCUMENTATION.md) document.


**Who is Predator designed for?**

Predator is designed for hobbyists and tech enthusiasts who want to experiment with ALPR without the need for expensive software and specialized equipment. It's for people who want to tinker and experiment with computer vision technology in a powerful and easy way.


**Can Predator be used as a plain dashcam, without ALPR?**

Absolutely. Predator's dashcam mode allows it to operate like a fully featured traditional dashcam, without any ALPR functionality. If you want to retroactively run ALPR on recorded dashcam video, you can do so using pre-recorded mode at a later time.


**What is Predator Apex?**

Predator Apex is the paid support program behind the Predator software. Predator Apex uses the exact same, free and open source Predator software that everyone else has access to. Predator Apex customers get one-on-one tech support and/or pre-built hardware devices. This service is available both to commercial customers and individual users. To learn more, you can contact V0LT using the information found at <https://v0lttech.com/contact.php>


**I have a problem with Predator and I need help.**

If you're encountering an issue with Predator, first ensure that you've followed all of the steps described in the [DOCUMENTATION.md](DOCUMENTATION.md). If your issue persists, try to work out its source by checking individual potential points of failure. The majority of Predator issues can be traced back to one of its dependencies not working properly. Check that the ALPR engine, FFMPEG, and GPSD are all working properly. If you still can't resolve your issue, you can contact V0LT support using the information found at <https://v0lttech.com/contact.php>.


**How is Predator related to OpenALPR?**

Predator's intended ALPR engine, Phantom, is heavily based on OpenALPR. Predator can also be configured to use OpenALPR directly as its ALPR back-end.


**What advantages does Phantom have as an ALPR back-end over OpenALPR?**

Using Phantom as the ALPR back-end over OpenALPR is recommended for a few reasons. Phantom returns much more computer-friendly errors, meaning Predator can more reliably detect when the ALPR engine encounters problems, and can provide more actionable solutions. Additionally, Phantom's "video transparency" allows other processes to access images captured by the ALPR process. This allows Predator to run object recognition using the same camera used by the ALPR process.


**Who is Predator not designed for?**

Predator is not designed for those who want to conduct mass-surveillance. Its not for governments and law enforcement agencies looking to log the movements of civilians for criminal investigations. Its not for companies who want to track how often certain people visit their business. For sake of privacy, Predator actively avoids features designed for mass-surveillance, and focuses on targeted, private alerts for individual use.


**How much does Predator cost?**

The Predator software itself is completely free, and has absolutely no subscriptions. However, you may still need to purchase hardware for Predator to run on. You can either assemble hardware yourself, or purchase pre-made models through Predator Apex (see [APEX.md](APEX.md))


**What operating systems is Predator compatible with?**

Officially, Predator is only compatible with Linux based operating systems, and is primarily designed for Debian-based distributions (though other distributions should work smoothly as well). However, if you're OK with a few hiccups, its also reasonably possible to install Predator on MacOS. Since Predator and all of its dependencies are all open source, it's technically possible to get it to work on Windows as well, but but you'll have to re-write a significant portion of it to get everything working as intended. In short, Predator on Linux works great, Predator on MacOS will probably work, and Predator in Windows would take extensive effort and modifications.


**Why is Predator written in Python, and not something more efficient, like C++?**

Python makes the development of the core Predator system much faster and more efficient. Additionally, Python makes it much easier to port Predator to new platforms. While Predator itself is indeed written in Python, many of its processing-heavy dependencies are written in C++. For example, Phantom, Predator's ALPR engine, is written in C++. This allows the system as a whole to benefit from the convenience of Python, without significantly harming processing performance of critical processes.


**How does Predator work?**

Predator is a fairly complex program, but below is a list of the general steps Predator takes when processing video, whether it be in real-time or a pre-recorded sample.

1. Depending on the mode, Predator will either load a pre-recorded video, or connect to a live camera to stream images.
2. Predator then splits the video, regardless of its source, into individual frames at a semi-regular interval.
3. Next, Predator might crop each frame down based on its configuration in order to remove unnecessary data.
4. Next, Predator's ALPR engine attempts to locate all potential plates.
5. Next, Predator's ALPR engine attempts interpret the plates detected, and makes a guess as to their contents.
6. After the ALPR engine finishes, Predator forms a list of the most likely plates guesses.
7. Predator then uses various methods of validation to filter out plate guesses that are unlikely to be correct.
8. Next, Predator removes plates it believes to be invalid, and creates a list of (ideally) correctly recognized plates.
9. Finally, Predator checks the list of license plates against any alert lists that may be loaded to check for hot-list hits.
9. After this, Predator might save the plates to a local log file, send a push notification to a Gotify server, play an audio alert, or any number of other customizable actions.


**How many cameras can Predator use at one time?**

This is a bit of a complex question, but in short, as many as you want. More specifically, Predator will use as many cameras as your OS, USB controller, and processor allow. In practice, this means that Predator can usually run at least two USB cameras at once, even on low powered devices like the Raspberry Pi. However, you should keep in mind that adding more cameras will increase the processing load significantly. As such, you should expect a decrease in frame-rate for each camera you add, unless you have plenty of processing head-room.


**Can I run multiple instances of Predator at the same time on a single device?**

Theoretically, yes. However, this could easily cause several issues. For example, 1 camera device can only be used by a single process at a time, so running multiple instance of Predator could cause one or both instances to fail. If you want to run two instances of Predator at the same time, then you're much more likely to have success if each instance is running in a different mode. For example, running one instance of real-time mode in the background with an instance of pre-recorded mode in the foreground will almost certainly work just fine.
