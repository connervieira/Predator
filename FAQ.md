# Frequently Asked Questions

This document contains a series of questions you may have concerning Predator.

**What is Predator?**

    In short, Predator is a utility for detecting license plates, both in real-time, and by scanning a pre-recorded video. Predator is also capable of general object recognition, and can identify objects like vehicles, traffic lights, pedestrians, and dozens of others.

**How do I install Predator?**

    For installation and setup instructions, check tte DOCUMENTATION.md document.

**I have a problem with Predator and I need help.**

    If you're encountering an issue with Predator, first ensure that you've followed all of the steps described in the `DOCUMENTATION.md` document for setting up Predator. If your issue persists, try to work out its source. The majority of Predator issues can be traced back to one of it's dependencies not working properly. Check that OpenALPR, FSWebcam, and FFMPEG are all working properly. If you still can't resolve your issue, contact V0LT support using the information found at <https://v0lttech.com/contact.php>. From there, you can find various contact methods for V0LT, including instant messaging over Matrix, and email with optional PGP encryption.

**Who is Predator designed for?**

    Predator is designed for hobbyists, tech enthusiasts, and regular individuals. It's designed for those who are curious about how many cars they pass, and for those who want a customizable, extensible camera platform to build on top of. It's for those who want to log everyone who enters their driveway, and for those who want alerts when their friends and family arrive at their house. It's for people who want to tinker and experiment with computer vision technology in a powerful and easy way.

**Who is Predator not designed for?**

    Predator is not designed for those who want to collect massive amounts of information on individuals. It's not for governments and law enforcement agencies looking to track the movements of civilians. It's not for companies who want to monitor how often certain people visit their business. For sake of privacy, Predator actively avoids features designed for mass-surveillance.

**Doesn't Predator encourage mass-surveillance, and therefore violate the philosophy of V0LT?**

    While Predator is technically a surveillance program, it's designed intentionally to excel at things an individual user would find helpful without benefitting those who want to collect massive quantities of information. For example, Predator doesn't have any native crowd-sourcing features that could serve to collect information from all over a region. Predator also can only detect a single license plate per frame it analyzes, meaning it should work great for the average driver scanning the cars they pass, but not benefit someone looking to scan 20 cars at once as they drive through an intersection. That all being said, there is absolutely a possibilty that Predator could be used for surveillance. However, there are dozens of pre-existing services that could already do this. To put it another way, someone who wants to collect information on thousands of people would almost certainly use an ALPR other than Predator; one designed more with this purpose in mind.

**How much does Predator cost?**

    The Predator software itself is completely free, and has absolutely no subscriptions. However, you may still need to purchase hardware for Predator to run on. You can either assemble hardware yourself, or purchase pre-made models through Predator Apex (see APEX.md)

**What operating systems is Predator compatible with?**

    Officially, Predator is only compatible with Linux based operating systems, and is primarily designed for Debian based distributions (though other distributions should work smoothly as well). However, if you're ok with a few hiccups, its also reasonably possible to install Predator on MacOS. Since Predator and all of its dependencies are all open source, it's technically possible to get it to work on Windows, but you'll have to re-write a significant portion of it to get everything working as intended. In short, Predator on Linux works great, Predator on MacOS will probably work, and Predator in Windows would take extensive effort and modifications.

**Why is Predator written in Python, and not something more efficient, like C++?**

    While Predator itself is indeed written in Python, many of it's dependencies are written in C++. OpenALPR, the core of Predator's backend, is written in C++. This way, the Predator front-end benefits from the simplicity and compatibility of Python, while it's back-end benefits from the performance of C++.

**How can I get Predator to automatically open gates, turn on lights, or complete other automation related tasks?**

    For starters, Predator should never be used for security or safety critical tasks. However, if this is something you'd like to do in a non critical situation, and you fully understand that Predator is not infallable, you can configure Predator submit data about the plates it detects in real-time mode to a webhook. This webhook can be used to integrate Predator with a home automation system or other similar set-up. For more information on how this process works, see the `CONFIGURATION.md` document.

**How does Predator work?**

    Predator is a fairly complex program, but below is a list of the general steps Predator takes when processing video, whether it be in real-time or a pre-recorded sample.

    1. Depending on the mode, Predator will either load a pre-recorded video, or connect to a camera and stream video that way.
    2. Predator then splits the video, regardless of its source, into individual frames at a regular interval.
    3. Next, Predator crops each frame down based on its configuration in order to remove unnecessary data.
    4. Next, Predator uses OpenALPR to locate all potential plates.
    5. Next, Predator uses OpenALPR to interpret the plates detected, and makes a guess as to their contents.
    6. After OpenALPR finishes, Predator forms a list of the most likely plates guesses.
    7. Predator then uses various methods of validation to filter out plates that are unlikely to be correct.
    8. Finally, Predator removes plates it believes to be invalid, and creates a list of (hopefully) correctly detected plates.
    9. After this, Predator might save the plates to a database, send a push notification to a Gotify server, play an audio alert, any any number of other customizable actions.

**How many cameras can Predator use at one time?**
    This is a bit of a complex question, but in short, as many as you want. More specifically, Predator will use as many cameras as your OS, USB controller, and processor allow. In practice, this means that Predator can usually run at least two USB cameras at once, even on low powered devices like the Raspberry Pi.
