# Changelog

## 0.9.0
Allow custom subclasses to be used when deserializing data. This allows
customization of how the deserialized data is handled without having to resort
to monkey patching r_map's classes directly.

## 0.8.0
Fixed an issue with arrayed nodes where the starting index wasn't being respected
Fix handling of deep_copy when it's not requested
