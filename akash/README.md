# Deployment on Akash

What better way to deploy an open source public goods project than on
a decentralized permissionless platform?

The [Akash][akashnet] network is an open marketplace for computing
resources powered by web3.

[akashnet]: https://akash.network/

## Steps

### 1. Get a Chat API key

Go to the [Akash Chat API page][akashchatapi] and click Get Started.
You'll fill in a few details then be able to generate the key.

[akashchatapi]: https://chatapi.akash.network/

### 2. Set up your wallet

Follow [these][wallet] instructions to set up your Cosmos wallet. This
is necessary to be able to bid for compute resources in the Akash
network.

[wallet]: https://akash.network/docs/getting-started/token-and-wallets/

### 3. Deploy the app on the Akash Console

Head over to the [Akash console][akashconsole] and connect your wallet.

[akashconsole]: https://console.akash.network/

Select the 'Deployments' menu option and click 'Deploy' then 'Upload your SDL'.

Select [this](sdl.yaml) file from where you've cloned the repository.

You can then specify the API key you generated in step 1 above, and
optionally change the model name. Available models can be found
[here][supported-models]

[supported-models]: https://chatapi.akash.network/documentation

Finally, click 'Create Deployment'. You'll be asked to deposit
a small amount of tokens from your wallet then shown bids from
the available providers.

Select one provider and confirm the transaction from your wallet then
the deployment will begin.

After a couple of minutes or so, when you head to 'Deployments' you'll
find the deployment completed and clicking on it, you'll get access
to the link that loads the application.
