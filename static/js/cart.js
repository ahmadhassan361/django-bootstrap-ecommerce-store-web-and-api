// console.log(user);
// var updateBtns = document.getElementsByClassName("add-to-cart")
// get_cart_total();
// for(var i=0;i<updateBtns.length ; i++){
//     updateBtns[i].addEventListener('click',function(){
//         var productId = this.dataset.product
//         var action = this.dataset.action
//         console.log("productId:",productId," action:",action)
//         addProduct(productId,action,1)
//         get_cart_total();


//     })
// }




// function addProduct(productId,action,quantity){

//     if(action === "add"){

//         if(localStorage.getItem("cart-items") === null){
        
//             let item = {
//             productId:productId,
//             quantity:quantity
//             }
//             let cart_item_list = []
//             cart_item_list.push(item)
//             localStorage.setItem("cart-items",JSON.stringify(cart_item_list))
//             console.log("1st item added ")
            
//         }else{

//             let cart_item_list =   JSON.parse(localStorage.getItem("cart-items"));
//             let find = false
//             let index = -1
//             for(var i=0;i<cart_item_list.length; i++){
//                 if(cart_item_list[i].productId == productId){
//                     find = true
//                     index = i
//                 }
//             }
//             if(find && index !=-1){
//                 cart_item_list[index].quantity +=1;
//                 localStorage.setItem("cart-items",JSON.stringify(cart_item_list))
//                 console.log("quantity increases")
//             }else{
//                 let item = {
//                     productId:productId,
//                     quantity:parseInt(quantity)
//                 }
//                 cart_item_list.push(item)
//                 localStorage.setItem("cart-items",JSON.stringify(cart_item_list))
//                 console.log("item added")

//             }
//         }

        
//     }else if(action === 'remove'){
//         let cart_item_list =   JSON.parse(localStorage.getItem("cart-items"));
//             let find = false
//             let index = -1
//             for(var i=0;i<cart_item_list.length; i++){
//                 if(cart_item_list[i].productId == productId){
//                     find = true
//                     index = i
//                 }
//             }
//             if(find && index !=-1){
//                 if(cart_item_list[index].quantity > 1){
//                     cart_item_list[index].quantity -=1;
//                 localStorage.setItem("cart-items",JSON.stringify(cart_item_list))
//                 console.log("quantity decrease")
//                 }
                
//             }
//     }






// }
// function addProductCart(productId,action,quantity){ //details page

//     if(action === "add"){

//         if(localStorage.getItem("cart-items") === null){
        
//             let item = {
//             productId:productId,
//             quantity:parseInt(quantity)
//             }
//             let cart_item_list = []
//             cart_item_list.push(item)
//             localStorage.setItem("cart-items",JSON.stringify(cart_item_list))
//             console.log("1st item added ")
            
//         }else{

//             let cart_item_list =   JSON.parse(localStorage.getItem("cart-items"));
//             let find = false
//             let index = -1
//             for(var i=0;i<cart_item_list.length; i++){
//                 if(cart_item_list[i].productId == productId){
//                     find = true
//                     index = i
//                 }
//             }
//             if(find && index !=-1){
//                 cart_item_list[index].quantity = parseInt(quantity) + parseInt(cart_item_list[index].quantity);
//                 localStorage.setItem("cart-items",JSON.stringify(cart_item_list))
//                 console.log("quantity increases")
//             }else{
//                 let item = {
//                     productId:productId,
//                     quantity:parseInt(quantity)
//                 }
//                 cart_item_list.push(item)
//                 localStorage.setItem("cart-items",JSON.stringify(cart_item_list))
//                 console.log("item added")

//             }
//         }

        
//     }else if(action === 'remove'){
//         let cart_item_list =   JSON.parse(localStorage.getItem("cart-items"));
//             let find = false
//             let index = -1
//             for(var i=0;i<cart_item_list.length; i++){
//                 if(cart_item_list[i].productId == productId){
//                     find = true
//                     index = i
//                 }
//             }
//             if(find && index !=-1){
//                 if(cart_item_list[index].quantity > 1){
//                     cart_item_list[index].quantity -=1;
//                 localStorage.setItem("cart-items",JSON.stringify(cart_item_list))
//                 console.log("quantity decrease")
//                 }
                
//             }
//     }






// }

// function get_cart_total(){
//     if(localStorage.getItem("cart-items") === null)
//     {
        
//         document.getElementById("cart-badge").innerHTML = "0"
//     }else{
        
//         let cart_list =  JSON.parse(localStorage.getItem("cart-items"))
//          document.getElementById("cart-badge").innerHTML = cart_list.length.toString()
//     }
// }


