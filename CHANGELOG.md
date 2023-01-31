# Changelog
*All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [Unreleased]

#### Changed

- Updated the legacy `_learnq` js object to the new `klaviyo` js object.

### [3.0.7] - 2023-01-24

#### Changed

- Updated "Tested up to" from 6.0.1 => 6.1.1

### [3.0.6] - 2023-01-03
#### Fixed
- Undefined categories in cart rebuild.
- Added ProductID to viewed product events for better integration with product recommenders.

### [3.0.5] - 2022-12-08

#### Fixed

- Prevent automatic integration removal.

#### Removed

- Sending webhook on plugin deactivation.

### [3.0.4] - 2022-10-20

#### Fixed

- Removed product description from the kl_build_add_to_cart_data method to reduce the size of the payload.

- Started Checkout events not working with TT2 theme

##### Changed
- Use POST instead of GET when sending through Added to Cart Event.

### [3.0.3] - 2022-04-12
##### Changed
- Query only for product post_type at klaviyo/v1/products resource.
- Use get_home_url() for url query param in auth/handle request.

### [3.0.2] - 2022-03-28
##### Changed
- Assets for brand refresh.

##### Fixed
- Undefined index warnings in cart build.

### [3.0.1] - 2022-02-07
##### Fixed
- Remove redirect after update/install.

### [3.0.0] - 2022-02-07
##### Added
- Options endpoint supporting GET/POST requests.
- Improved validation function for custom endpoints.
- `is_most_recent_version` key to the response from the /klaviyo/v1/version endpoint detailing whether plugin update is available.
- Webhook service for outgoing requests to Klaviyo's webhook endpoint.
- Redirect to Klaviyo settings page after activation.
- Deactivation logic removing options, webhooks and sending request to Klaviyo to keep integration state aligned.
- WCK_Options class to handle deprecated options and adjusting via filter.
- `disable` endpoint to handle plugin data cleanup and deactivation when removed in Klaviyo.

##### Changed
- Updated plugin settings page allowing for management of settings in Klaviyo. Maintain original for non-WooCommerce sites.
- Use __DIR__ to define KLAVIYO_PATH constant for test compatibility.

##### Fixed
- PHP Notices on admin page when initial options are not set.

##### Deprecated
- Removed 'klaviyo_popup' and 'admin_settings_message' from `klaviyo_settings` option.

### [2.5.5] - 2021-12-09
##### Fixed
- Support for Synching Product Variations.

### [2.5.4] - 2021-11-10
##### Changed
- Default SMS consent disclosure text

### [2.5.3] - 2021-10-27
##### Fixed
- Over representation of cart value in Added to Cart events.

### [2.5.2] - 2021-08-10
##### Added
- Support for Chained Products

##### Deprecated
- Displaying Email checkbox on checkout pages based on ListId set in Plugin settings. This will be displayed using the Email checkbox setting on the Plugin settings page, as done for SMS checkout checkbox

### [2.5.1] - 2021-07-23
- Adjusted add to cart hook priority to allow for line item calculations

### [2.5.0] - 2021-07-12
##### Added
- Add to Cart event.

### [2.4.2] - 2021-06-16
#### Added
- Use exchange_id for "Started Checkout" if available

#### Changed
- Lowered priority of consent checkboxes to address conflicts with some checkout plugins

### [2.4.1] - 2021-04-14
##### Fixed
- Address console error faced while displaying deprecation notice on plugin settings page.

### [2.4.0] - 2021-03-17
##### Added
- Class to handle Plugins screen update messages.
- Collecting SMS consent at checkout.

##### Changed
- Refactor adding checkout checkbox to allow for re-ordering in form.
- Plugin settings form redesigned to be more intuitive.
- Enqueue Identify script before Viewed Product script.
- Moving to webhooks to collect Email and SMS consent.

##### Fixed
- Remove unnecessary wp_reset_query call in Klaviyo analytics.
- Move _learnq assignment outside of conditional in identify javascript.
- Assign commenter email value for localization.

### [2.3.6] - 2020-10-27
##### Fixed
- Remove escaping backslashes from Started Checkout product names.

##### *NOTE
- This CHANGELOG was created on 2020-12-01. For information on earlier versions please refer to the [plugin's readme.txt](https://github.com/klaviyo/woocommerce-klaviyo/blob/master/readme.txt).


[Unreleased]: https://github.com/klaviyo/woocommerce-klaviyo/compare/3.0.7...HEAD
[3.0.7]: https://github.com/klaviyo/woocommerce-klaviyo/compare/3.0.6...3.0.7
[3.0.6]: https://github.com/klaviyo/woocommerce-klaviyo/compare/3.0.5...3.0.6
[3.0.5]: https://github.com/klaviyo/woocommerce-klaviyo/compare/3.0.4...3.0.5
[3.0.4]: https://github.com/klaviyo/woocommerce-klaviyo/compare/3.0.3...3.0.4
[3.0.3]: https://github.com/klaviyo/woocommerce-klaviyo/compare/3.0.2...3.0.3
[3.0.2]: https://github.com/klaviyo/woocommerce-klaviyo/compare/3.0.1...3.0.2
[3.0.1]: https://github.com/klaviyo/woocommerce-klaviyo/compare/3.0.0...3.0.1
[3.0.0]: https://github.com/klaviyo/woocommerce-klaviyo/compare/2.5.5...3.0.0
[2.5.5]: https://github.com/klaviyo/woocommerce-klaviyo/compare/2.5.4...2.5.5
[2.5.4]: https://github.com/klaviyo/woocommerce-klaviyo/compare/2.5.3...2.5.4
[2.5.3]: https://github.com/klaviyo/woocommerce-klaviyo/compare/2.5.2...2.5.3
[2.5.2]: https://github.com/klaviyo/woocommerce-klaviyo/compare/2.5.1...2.5.2
[2.5.1]: https://github.com/klaviyo/woocommerce-klaviyo/compare/2.5.0...2.5.1
[2.5.0]: https://github.com/klaviyo/woocommerce-klaviyo/compare/2.4.2...2.5.0
[2.4.2]: https://github.com/klaviyo/woocommerce-klaviyo/compare/2.4.1...2.4.2
[2.4.1]: https://github.com/klaviyo/woocommerce-klaviyo/compare/2.4.0...2.4.1
[2.4.0]: https://github.com/klaviyo/woocommerce-klaviyo/compare/2.3.6...2.4.0
[2.3.6]: https://github.com/klaviyo/woocommerce-klaviyo/commit/a284a424df9fe41121f5101b9a9471aa91fad7c4
