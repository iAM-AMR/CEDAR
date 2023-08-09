

/* Scripts for data extraction templates. */

 /* Disable scrolling in active numeric field to prevent inadvertant updates 
    during navigation. */
 document.addEventListener("wheel", function(event){
    
        if(document.activeElement.type === "number"){
            document.activeElement.blur();
          }
    }

);