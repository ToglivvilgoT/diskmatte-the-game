# Template for skins metadata

The metadata.json file will be formatted as a list with objects.
Each objects represents a skin with the required values.
Each skin representing object will have the following format:

```json
{
    "name": "String",
    "slug": "SlugField",
    "description": "String",
    "price": "PositiveInteger",
    "kind": "COLOR" | "IMAGE" | "CSS_CLASS",
    "color": "#ffffff" | "#fff" | "rgb(123, 123, 123)",
    "image": "FilePath",
    "css_class": "String"
}
```

`name`, `slug`, `description`, `price` and `kind` are always required.
`color` is required when `kind = "COLOR"`
`image` is required when `kind = "IMAGE"`
`css_class` is required when `kind = "CSS_CLASS"`, and must match a class defined in `static/css/skins.css`

When loading the skins into database:
if all metadata fields are correctly present for a skin,
it can be inserted and marked as available.
If some or all fields are missing, populate the database
with placeholder or default values and mark the skin as not available.
An admin will then have to later manually add the missing fields.
