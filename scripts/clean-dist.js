const fs = require('fs');
const path = require('path');

const distPath = path.join(process.cwd(), 'dist');

fs.rm(distPath, { recursive: true, force: true }, (err) => {
    if (err) {
        console.error(`Error removing directory ${distPath}: ${err}`);
    } else {
        console.log(`Removed directory ${distPath}`);
    }
});
