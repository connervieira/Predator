# Debugging

This document explains the debug message system built into Predator, and how you can use it effectively to solve problems and improve efficiency.

1. Enable debugging messages.
    - To enable debugging messages, enable the `general>display>debugging_output` configuration value.
2. Run Predator.
    - After enabling debug messages, run Predator. You should see frequent grayed-out messages being printed to the console indicating important events behind the scenes.
3. Interpret messages.
    - Debugging messages may look complicated, but they follow a consistent structure: `[current_time] ([time_since_last_message] - [thread_name]) - [message]`
        - [current_time] is a Unix timestamp of the exact time the message was printed.
        - [time_since_last_message] is the length of time in seconds since the last message in the thread was printed.
        - [thread] is the name of the thread that the message was printed from.
        - [message] is the message itself.
    - Example: `1697686012.6295320988 (0.0000085831 - Main) - Processing ALPR alerts`
4. Locate source of delay.
    - One of the most useful implications of debugging messages is the ability to locate sources of delay during the operation of Predator.
    - To locate sources of slow-downs, you can use the `[time_since_last_message]` field described above.
        - This field will show how long the previous action in the thread took.
            - To clarify, processes in different threads work independently, and often run concurrently.
            - To locate sources of slow downs in a particular thread, pay attention to a specific thread's debug messages, and ignore other threads.
                - For example, to find slow downs in the "Main" thread, pay attention to messages marked as "Main", and ignore "ALPRStream" and "ALPRStreamMaintainer".
    - Example:
        1. Here's an example debug message sequence:
            - `1697686011.2565226555 (0.1619987488 - Main) - Loading networking libraries`
            - `1697686011.2566270828 (0.0000023842 - Main) - Loading ignore lists`
            - `1697686014.2589059357 (3.0022788525 - Main) - Initial loading complete`
        2. You'll notice that the time since the last message shown in the last line is just over 3 seconds.
            - This means that the previous action in the thread (in this case, loading the ignore lists), took 3 seconds.
        3. Resolve unnecessary delays.
            - After finding sources of delay, you may want to research their causes and attempt to resolve them.
            - In this example, the loading process for the ignore lists might be taking longer than expected because Predator doesn't have a reliable internet connection to download ignore lists from remote sources.
