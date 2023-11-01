# Facebook Account Checker

Facebook Account Checker is a Python application used to verify the status of Facebook accounts, whether they are live, checkpointed, or dead. This program can be used to check the security of your own accounts or understand the status of a specific Facebook account.

## Features

- Fast and multithreaded account checking.
- Ability to distinguish between live, checkpointed, and dead accounts.
- Saving live and checkpointed accounts to "live.txt" and "CheckPoint.txt" files.
- Saving dead accounts to the "check.txt" file.

## Installation

1. Install the required Python packages:

   ```
   install.bat
   ```

2. Add the Facebook accounts you want to check to the `account.txt` file, with one account per line.

3. Update the `proxy.txt` file to provide suitable proxies, or download proxies from online sources.

4. Run the code:

   ```
   python facebook-checker-v2.py
   ```

## Usage

- The program automatically checks each account and records the results in the "live.txt," "CheckPoint.txt," and "check.txt" files.
- Live accounts can be found in the "live.txt" file, checkpointed accounts in the "CheckPoint.txt" file, and dead accounts in the "check.txt" file.

## Contribution

If you would like to contribute, please submit a pull request for adding new features or fixing bugs. You can also open an issue for any feedback or questions.

## License

This project is licensed under the MIT License. For more information, see the [LICENSE](LICENSE) file.

---

Feel free to use this project as a starting point for your own enhancements or customizations. Happy coding!
```
