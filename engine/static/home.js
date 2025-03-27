var downloadlist = JSON.parse(localStorage.getItem("downloadlist")) || []; // array de titulos, salva no localStorage

function addQueue (title_name) { // adds titles to queue, no duplicates.
    console.log(`trying to add ${JSON.stringify(title_name)} to queue`)

    if (downloadlist.includes(title_name)){
        console.log(`${JSON.stringify(title_name)} already in queue`);
    }
    else {
        downloadlist.push(String(title_name)) // needs to be str only
        localStorage.setItem("downloadlist", JSON.stringify(downloadlist)) // salva no local storage
        console.log(`New download queue: ${downloadlist.toString()}`);
    };
};

async function downloadButton(download_array){
  var function_lock = true
  // sends title json to backend 
  try {
    const rqst = new Request("/download", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify(downloadlist),
    });
  
    const response = await fetch(rqst);

    if(!response.ok){
      throw new Error(`Error, Status: ${response.status}`);
      function_lock = false
    }

    const result = await response.json();
    console.log("Server resp:", result);
    localStorage.removeItem("downloadlist");
    downloadlist.length = 0;
    function_lock = false
  } catch (error) {
    console.error("error:", error);
  }
  
};