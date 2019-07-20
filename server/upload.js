const IncomingForm = require("formidable").IncomingForm;
const fs = require('fs');
const mv = require('mv');
const path = require('path');
const extract = require('extract-zip');
const spawn = require('child_process').spawn;

var upload_path = __dirname + '/uploads/';
var image_path = __dirname + '/images/';
var python_script = __dirname + '/sort_images.py';
var sorted_zip = __dirname + '/sorted.zip';

module.exports = function upload(req, res) {
  var form = new IncomingForm();
  form.on("file", (field, file) => {
        var args = {};
        console.log(image_path);
        console.log(python_script);
        args['temp_upload_path'] = file.path;
        args['uploaded_file'] = upload_path + file.name;
        args['extension'] = path.extname(args['uploaded_file']);
        args['file_name'] = path.basename(args['uploaded_file'], args['extension']);
        main(args);
        console.log('test');
  });

  form.on("end", () => {
    res.json();
  });
  form.parse(req);
};

function move_file(source, dest) {
    return new Promise((resolve, reject) => {
      console.log('moving filing');
      mv(source, dest, function (err) {
        if (err) throw err;
        return resolve(true);
      });
    });
  };
  
function move_folder(source, dest, file_name) {
    return new Promise((resolve, reject) => {
    console.log('moving folder');
    mv(source + file_name, dest, {clobber: false, mkdirp: true}, function (err) {
        if (err) throw err;
        return resolve(true);
    });
    });
};

function unzip_file(source, dest) {
    return new Promise((resolve, reject) => {
    console.log('unzipping file');
    extract(source, {dir: dest}, function (err) {
        if (err) throw err;
        return resolve(true);
    });
    });
};

function is_zip(extension) {
    return new Promise((resolve, reject) => {
    const zip_ext_list = ['.7z', '.zip', '.gzip'];
    if (zip_ext_list.indexOf(extension) > -1) {
        return resolve(true);
    }
    });
};

function sort() {
    return new Promise((resolve) => {
    console.log('running python script');
    const pythonProcess = spawn('python',[python_script]);
    return resolve(true);
    });
};

function send_file() {
    return new Promise((resolve) => {
    return resolve(true);
    });
};

async function main(...args) {
    var args = args[0];
    var l = [];
    let mv_file = await move_file(args['temp_upload_path'], args['uploaded_file']);
    let zip = await is_zip(args['extension']);
    if (zip) {
    let extract = await unzip_file(args['uploaded_file'], upload_path);
    let move_dir = await move_folder(upload_path, image_path, args['file_name']);
    let sort_stuff = await sort();
    return true;
    }
};