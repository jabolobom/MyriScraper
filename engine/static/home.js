const downloadlist = [];// array de titulos

function addQueue (title_name) { // adds titles to queue, no duplicates.
    console.log(`trying to add ${title_name} to queue`)
    if (downloadlist.includes(title_name)){
        console.log(`${title_name} already in queue`);
    }
    else {
        downloadlist.push(title_name)
        print(`New download queue: ${downloadlist.toString()}`);
    };
};

function downloadButton(download_array){
  // sends title json to backend 
  const rqst = new Request("/download", {
    method: "POST",
    body: JSON.stringify(downloadlist),
  });
};