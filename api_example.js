#!/usr/bin/node

const fetch = require('node-fetch');
const fs = require('fs');

fs.readFile('static/images/index.jpeg', 'base64', (error, img) => {
  if (error) {
    console.log(error);
  } else {
    fetch('https://haddy-catdenfy.hf.space/run/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        data: [
          'data:image/png;base64,' + img
        ]
      })
    })
      .then(r => r.json())
      .then(
        r => {
          const data = r.data[0];
          //   console.log(data.label.replace('_', ' '));
          //   console.log(data.confidences);
          const probsDict = {};
          for (let i = 0; i < data.confidences.length; i++) {
            probsDict[data.confidences[i].label.replace('_', ' ')] = data.confidences[i].confidence;
          }
          console.log('probability dictionary: ', probsDict);
          console.log('predicted class: ' + data.label);
        }
      );
  }
});
