# ROMs Module

This module is responsible for managing ROMs in the lifelog project.

## Features

- Add new ROMs
- List all available ROMs
- Delete ROMs
- Update ROM details

## Installation

To install the ROMs module, run the following command:

```bash
npm install lifelog-roms
```

## Usage

Here is an example of how to use the ROMs module:

```javascript
const roms = require('lifelog-roms');

// Add a new ROM
roms.add({ name: 'Super Mario', platform: 'NES' });

// List all ROMs
const allRoms = roms.list();
console.log(allRoms);

// Delete a ROM
roms.delete('Super Mario');

// Update ROM details
roms.update('Super Mario', { platform: 'SNES' });
```

## License

This project is licensed under the MIT License.