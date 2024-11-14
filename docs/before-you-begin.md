# Before You Begin

1. This project was created using Python v3.12, but should work with Python versions >= 3.10
2. Install the 
[KitOps Command-Line Interface (CLI)](https://kitops.ml/docs/cli/installation.html)
    - To determine if the Kit CLI is installed in your environment, do the   following:
        1. Open a Terminal window
        2. Run the following command:
            ```bash
            kit version
            ```
        3. You should see output similar to the following:
        
            Version: 0.4.0<br>
            Commit: e2e83d953823ac35648f2f76602a0cc6e8ead819<br>
            Built: 2024-11-05T20:29:07Z<br>
            Go version: go1.22.6<br>


3. If you haven't already done so, [sign up for a free account with Jozu.ml](https://api.jozu.ml/signup)
4. In the root directory of your project--which we'll call the *Project directory*--create a `.env` file.
5. Edit your `.env` file by adding an entry for your **JOZU_USERNAME**, your **JOZU_PASSWORD** and your **JOZU_NAMESPACE** (aka your **Personal Organization** name). For example:

        JOZU_USERNAME=brett@jozu.org
        JOZU_PASSWORD=my_password
        JOZU_NAMESPACE=brett

    - The Kitops Manager uses the entries in the `.env` file to login to [Jozu.ml](https://www.jozu.ml).
    - As an alternative to using a `.env` file, you can create Environment Variables for each of the entries above.
6. Be sure to save the changes to your .env file before continuing.

