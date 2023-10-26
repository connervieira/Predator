# Security

## Disclaimer

While Predator strives to be reliable and secure, you should not rely on it for safety critical tasks. Predator is designed to be an accessible hobbyist-level alternative to industrial license plate reading devices, and shouldn't be used to authenticate vehicles at entry points, or be the only line of defense in detecting criminal activity.


## Support

Due to Predator's update cycle, only the latest version receives security patches. However, in severe cases, patches for older version might be released on a case by case basis. Regardless, for the safest experience, you should always use the latest version of Predator.


## Reporting

In the event that you find a security issue with Predator, you have several ways of reporting it. The first, and safest option is to contact V0LT directly. You can find relevant contact information, including PGP keys at <https://v0lttech.com/contact.php>


## Considerations

Here are some security considerations you should account for before using Predator.

1. Assume anyone using a particular instance of Predator has full access to the system it's running on, regardless of the configuration.
    - Predator offers configuration values that allow an administrator to enable and disable individual modes. However, these configuration values should not be considered a security feature, since they can be easily bypassed by someone with access to the machine running Predator.
    - Predator also assumes information entered into prompts is safe, generally speaking. For example, Predator doesn't stop the user from entering ".." into file path prompts in order to access files outside of the root project directory.
        - Predator's input santization is designed to prevent common mistakes and improve Predator's stability, not to prevent a malicious user from compromising the system Predator is running on.
2. License plate recognition is not an exact science; don't depend on it for safety or security critical tasks.
    - Predator has features that make it possible to turn license plate detections into triggers for automation tasks. For example, it's possible to link Predator to a home automation program, and automatically open a gate when particular vehicle approaches. However, you should use extreme caution when using Predator in situations like this. You should not depend on accurate license plate readings for any safety or security critical task.
3. Predator is capable of collecting sensitive data, like GPS recordings, license plates, and dash-cam video. Make sure you take efforts to physically protect the system Predator is running on.
    - While you may be using good security practices when it comes to the software you're using, don't neglect the physical security of Predator. Realize that it's entirely possible for someone to take the storage medium Predator is running on, and steal the information off it.
    - While every situation is different, it's generally good practice to keep Predator's core processor installed in a private and secure location with full disk encryption enabled to reduce the risk of physical theft of data.
