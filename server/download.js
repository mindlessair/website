const IncomingForm = require("formidable").IncomingForm;
const fs = require('fs');
const mv = require('mv');
const path = require('path');
const extract = require('extract-zip');
const spawn = require('child_process').spawn;

var upload_path = __dirname + '\\uploads\\';
var image_path = __dirname + '\\images\\';
var python_script = __dirname + '\\sort_images.py';
var sorted_zip = __dirname + '\\sorted.zip';

module.exports = function download(req, res) {
    const file = `${__dirname}\\sorted.zip`;
    console.log(file);
    res.download(file);
    
};
