var downloadlist = JSON.parse(localStorage.getItem("downloadlist")) || []; // array de titulos, salva no localStorage

function addQueue (title_name) { // adds titles to queue, no duplicates.
    console.log(`trying to add ${title_name} to queue`)

    if (downloadlist.includes(title_name)){
        console.log(`${title_name} already in queue`);
    }
    else {
        downloadlist.push(title_name)
        localStorage.setItem("downloadlist", JSON.stringify(downloadlist)) // salva no local storage
        console.log(`New download queue: ${downloadlist.toString()}`);
    };
};

async function downloadButton(download_array){
  // sends title json to backend 
  try {
    const rqst = new Request("/download", {
      method: "POST",
      body: JSON.stringify(downloadlist),
    });
  
    const response = await fetch(rqst);

    if(!response.ok){
      throw new Error(`Error, Status: ${response.status}`;)    
    }

    const result = await response.json();
    console.log("Server resp:", result);
    // function body
  } catch (error) {
    console.error("error:", error);
  }
  
};