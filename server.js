const path = require("path");
const express = require("express");
const app = express(); // create express app


// add middlewares
app.use(express.static(path.join(__dirname,  "build")));
app.use(express.static("public"));
app.use((req, res, next) => {
  res.sendFile(path.join(__dirname,  "build", "index.html"));
});


app.listen(8080, console.log("connected at 8000"));