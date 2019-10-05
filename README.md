![logo](https://i.imgur.com/CNnILmD.png)

# OlivettiClub backend

Backend software for the OlivettiClub project @ Olivetti Hack Trento '19.

This is an HTTP Api that allows merchants to manage their coupons as part of the OlivettiClub network.
Specifically, it provides the following features:

* Merchants can register to the platform;
* Merchants can create coupons for the products they sell, and store them in the OlivettiClub cloud;
* Coupons have a limited availability, and each coupon can be redeemed only once;
* Coupons are distributed to other merchants that will give them to their customers.

At registration time, merchants are required to provide a number of information, such as their ATECO number
and their address, that are used by the AI engine.
Some additional data is also inferred, such as the geographic coordinates of a merchant, which are obtained
by the address provided.

An experimental feature is implemented to use an artificial intelligence engine to drive the distribution
of coupons, with the goal of maximizing the conversion rate and minimizing the chances to push customers
to competitor businesses.
Instructions to enable this feature are available below.

To learn about the usage of this API, refer to the `local_flow.sh` script, which showcases the standard
flow that is expected for this API.

This software is a proof of concept and it lacks some features that would be necessary in a real-world scenario,
such as authentication and error handling.

#### Usage

Install the required dependencies:

```bash
pip install flask pony geocoder requests
```

Run it locally:

```bash
flask run
```

Simulate a standard flow:

```bash
./local_flow.sh
```

Populate the database with example data:
```bash
./seed.sh
```

#### Enabling the AI engine

It is possible to enable the experimental AI engine by
setting the `AI_ENABLED` flag to True in `app.py`, and setting
the URL of the AI server with the `AI_URL` constant in `ai_utils.py`.

