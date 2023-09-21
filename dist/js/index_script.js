$(document).ready(function () {
    const nextButton = document.querySelector(`#next_button`);
    const previousButton = document.querySelector(`#previous_button`);
    const currentPageElement = document.querySelector(`#current_page`);
    const table = document.querySelector(`#data_table`);
    const titlePage = document.querySelector(`#title_page`);
    const titleOf = document.querySelector(`#title_of`);
    const totalPagesElement = document.querySelector(`#total_pages`);
    const currentPageNumberElement = document.querySelector(`#current_page_number`);
    const resultsNumber = document.querySelector(`#results_number`);
    const mainDashboard = document.querySelector(`#main_dashboard_table`);
    const registeredUsers = document.querySelector(`#registered_users`);
    const uploadedVideos = document.querySelector(`#uploaded_videos`);
    var previousText

    function formatCustomDate(apiDate) {
        const dateObj = new Date(apiDate);
        const hours = dateObj.getHours().toString().padStart(2, '0');
        const minutes = dateObj.getMinutes().toString().padStart(2, '0');
        const day = dateObj.getDate().toString().padStart(2, '0');
        const month = (dateObj.getMonth() + 1).toString().padStart(2, '0'); // Note: Months are 0-indexed, so add 1.
        const year = dateObj.getFullYear();
        return `${hours}:${minutes} - ${day}/${month}/${year}`;
    }

    function capitalizeFirstLetter(inputString) {
        return inputString.charAt(0).toUpperCase() + inputString.slice(1);
      }
    
    function loadVideoData(pageNumber) {
        $.ajax({
            url: 'videos/page=' + pageNumber,  
            method: 'GET',
            success: function (data) {
                $('#table_name').html('Videos List');
                var tableHeaders = '<th class="px-4 py-2 bg-gray-200 text-gray-800 border">Video ID</th><th class="px-4 py-2 bg-gray-200 text-gray-800 border">User ID</th>' +
                '<th class="px-4 py-2 bg-gray-200 text-gray-800 border">Status</th><th class="px-4 py-2 bg-gray-200 text-gray-800 border">Created At</th><th class="px-4 py-2 bg-gray-200 text-gray-800 border">Original Path</th>';
                $('#table_headers').html(tableHeaders);
                $('#data_table tbody').empty();
                currentPageElement.innerHTML = pageNumber;
                $('#current_page_number').html(pageNumber);
                $('#total_pages').html(data.num_pages);
                if(data.results.length == 0 || data.num_pages == 1){
                    nextButton.classList.add('hidden');
                    currentPageElement.classList.add('hidden');
                    if(data.results.length == 0) {
                        titlePage.classList.add('hidden');
                        titleOf.classList.add('hidden');
                        totalPagesElement.classList.add('hidden');
                        currentPageNumberElement.classList.add('hidden');
                        resultsNumber.innerHTML = "No videos found";
                    }
                    else {
                        titlePage.classList.remove('hidden');
                        titleOf.classList.remove('hidden');
                        totalPagesElement.classList.remove('hidden');
                        currentPageNumberElement.classList.remove('hidden');
                        resultsNumber.innerHTML = "Results: " + data.count;
                    }
                } else {
                    nextButton.classList.remove('hidden');
                    currentPageElement.classList.remove('hidden');
                    titlePage.classList.remove('hidden');
                    titleOf.classList.remove('hidden');
                    totalPagesElement.classList.remove('hidden');
                    currentPageNumberElement.classList.remove('hidden');
                    resultsNumber.innerHTML = "Results: " + data.count;
                }
                if(pageNumber == 1)
                previousButton.classList.add('hidden');
                if(pageNumber == data.num_pages)
                 { nextButton.classList.add('hidden'); }
                $.each(data.results, function (index, video) {
                    var videoStatusColor
                    var customDate = formatCustomDate(video.created_at);
                    var loadingIcon
                    if(video.status == 'pending') { 
                        videoStatusColor = 'yellow-500'
                        loadingIcon = '<lord-icon src="https://cdn.lordicon.com/xjovhxra.json"trigger="loop"colors="primary:#3080e8,secondary:#e8e230"stroke="80"style="width:22px;height:22px;top:4px;left:10px;"></lord-icon>'}
                    else if(video.status == 'completed') {
                        videoStatusColor = 'green-500'
                        loadingIcon = ""
                    }
                    else {
                        videoStatusColor = 'rose-500'
                        loadingIcon = ""
                    }
                    var row = '<tr class="text-center h-14">' +
                        '<td class="px-4 py-2 border text-center">' + video.id + '</td>' +
                        '<td class="px-4 py-2 border text-center">' + video.user_id + '</td>' +
                        '<td class="px-4 py-2 border text-center">' + '<h4 class="w-4/5 h-auto min-w-min rounded text-center text-outline-white-black font-medium bg-' + videoStatusColor + ' inline-block">' + capitalizeFirstLetter(video.status) + loadingIcon +'<h4></td>' +
                        '<td class="px-4 py-2 border text-center">' + customDate + '</td>' +
                        '<td class="px-4 py-2 border text-left truncate hover:text-clip">' + video.original_video_path+ '</td>' +
                        '</tr>';
                    $('#data_table tbody').append(row);
                });
            },
            error: function () {
                console.log('API request for videos failed');
            }
        });
    }

    // Function to load user data.
    function loadUserData(pageNumber) {   
        $.ajax({
            url: 'users/page=' + pageNumber,  // Replace with your API endpoint URL for users.
            method: 'GET',
            success: function (data) {
                $('#table_name').html('Users List');
                var tableHeaders = '<th class="px-4 py-2 bg-gray-200 text-gray-800 border">User ID</th><th class="px-4 py-2 bg-gray-200 text-gray-800 border">Email</th><th class="px-4 py-2 bg-gray-200 text-gray-800 border">Status</th><th class="px-4 py-2 bg-gray-200 text-gray-800 border">Action</th>';
                $('#table_headers').html(tableHeaders);
                $('#data_table tbody').empty();
                currentPageElement.innerHTML = pageNumber;
                $('#current_page_number').html(pageNumber);
                $('#total_pages').html(data.num_pages); 
                if(data.results.length == 0 || data.num_pages == 1){
                    nextButton.classList.add('hidden');
                    currentPageElement.classList.add('hidden');
                    if(data.results.length == 0) {
                        titlePage.classList.add('hidden');
                        titleOf.classList.add('hidden');
                        totalPagesElement.classList.add('hidden');
                        currentPageNumberElement.classList.add('hidden');
                        resultsNumber.innerHTML = "No users found";
                    }
                    else {
                        titlePage.classList.remove('hidden');
                        titleOf.classList.remove('hidden');
                        totalPagesElement.classList.remove('hidden');
                        currentPageNumberElement.classList.remove('hidden');
                        resultsNumber.innerHTML = "Results: " + data.count;
                    }
                } else {
                    nextButton.classList.remove('hidden');
                    currentPageElement.classList.remove('hidden');
                    titlePage.classList.remove('hidden');
                    titleOf.classList.remove('hidden');
                    totalPagesElement.classList.remove('hidden');
                    currentPageNumberElement.classList.remove('hidden');
                    resultsNumber.innerHTML = "Results: " + data.count;
                }
                if(pageNumber == 1)
                previousButton.classList.add('hidden');
                if(pageNumber == data.num_pages)
                { nextButton.classList.add('hidden'); }
                $.each(data.results, function (index, user) {
                    var userStatusColor = user.status == 'banned' ? 'rose-500' : 'green-500';
                    var buttonColor = user.status == 'banned' ? 'blue' : 'red';
                    var buttonContent = user.status == 'banned' ? '<i class="fa-solid fa-unlock"></i>' : '<i class="fa-solid fa-ban"></i>';
                    var row = '<tr class="text-center h-14" data-user-id="' + user.id + '">' +
                        '<td class="px-4 py-2 border text-center">' + user.id + '</td>' +
                        '<td class="px-4 py-2 border text-center">' + user.email + '</td>' +
                        '<td class="px-4 py-2 border text-center">' + '<h4 class="w-3/6 min-w-min rounded border text-outline-white-black font-medium bg-' + userStatusColor + ' inline-block">' + capitalizeFirstLetter(user.status) +'<h4></td>' +
                        '<td class="px-4 py-2 border text-center">' +
                            '<button class="w-18 h-18 rounded-lg bg-' + buttonColor + '-500 text-white py-1 px-3 rounded-full" onclick="banUser(' + user.id + ')" ' +
                             ' id="' + user.id + '">'+ buttonContent + '</button>' +
                        '</td>'+
                        '</tr>';
                    $('#data_table tbody').append(row);
                });                                       
            } ,
            error: function () {
                console.log('API request for users failed');
            }
        });
    }

    function getActiveCategory(activeCategory) {
        const tableName = document.querySelector(`#table_name`);
        const searchBar = document.querySelector(`#search_bar`);
        const pageCount = document.querySelector(`#page_count`);
        const pageNavigator = document.querySelector(`#page_navigator`);
        var videos_dashboard = document.getElementById("videos_dashboard_li");
        var users_dashboard = document.getElementById("users_dashboard_li");
        var home_dashboard = document.getElementById("home_dashboard_li");
        var searchInput = document.getElementById("search");
        searchInput.value = "";
        table.classList.remove('search_table')
        if(activeCategory == "videos_dashboard") {
            videos_dashboard.classList.remove('text-green-500');
            videos_dashboard.classList.add('bg-green-500');
            videos_dashboard.classList.add('text-white');
            users_dashboard.classList.remove('bg-green-500');
            users_dashboard.classList.remove('text-white')
            users_dashboard.classList.add('text-green-500');
            home_dashboard.classList.remove('bg-green-500')
            home_dashboard.classList.remove('text-white')
            home_dashboard.classList.add('text-green-500')
            table.classList.add('video_table')
            table.classList.remove('user_table')
            table.classList.remove('hidden')
            searchBar.classList.remove('hidden')
            pageCount.classList.remove('hidden')
            pageNavigator.classList.remove('hidden')
            tableName.classList.remove('hidden')
            mainDashboard.classList.add('hidden')
        }
        else if(activeCategory == "users_dashboard") {
            users_dashboard.classList.remove('text-green-500')
            users_dashboard.classList.add('bg-green-500')
            users_dashboard.classList.add('text-white')
            videos_dashboard.classList.remove('bg-green-500')
            videos_dashboard.classList.remove('text-white')
            videos_dashboard.classList.add('text-green-500')
            home_dashboard.classList.remove('bg-green-500')
            home_dashboard.classList.remove('text-white')
            home_dashboard.classList.add('text-green-500')
            table.classList.add('user_table')
            table.classList.remove('video_table')
            table.classList.remove('hidden')
            searchBar.classList.remove('hidden')
            pageCount.classList.remove('hidden')
            pageNavigator.classList.remove('hidden')
            tableName.classList.remove('hidden')
            mainDashboard.classList.add('hidden')
        }
        else {
            users_dashboard.classList.remove('text-green-500')
            home_dashboard.classList.add('text-white')
            home_dashboard.classList.add('bg-green-500')
            users_dashboard.classList.add('text-green-500')
            users_dashboard.classList.remove('bg-green-500')
            users_dashboard.classList.remove('text-white')
            videos_dashboard.classList.remove('bg-green-500')
            videos_dashboard.classList.remove('text-white')
            videos_dashboard.classList.add('text-green-500')
            table.classList.add('hidden')
            searchBar.classList.add('hidden')
            pageCount.classList.add('hidden')
            pageNavigator.classList.add('hidden')
            tableName.classList.add('hidden')
            mainDashboard.classList.remove('hidden')
        }
    }

    function getMainDashboardData() {
        $.ajax({ 
            url: 'page_info/',
            method: 'GET',
            success: function (data) {
                registeredUsers.innerHTML = data.Total_users;
                uploadedVideos.innerHTML = data.Total_videos;
            }
        })
    }
    
    getActiveCategory(home_dashboard)
    consoleText(['AnimeChan', 'Made with love ❤️'], 'text',['black', '#3498DB', 'tomato', '#F1C40F', '#2ECC71', '#2C3E50', '#AF7AC5', '#1A5276', '#EC2F07', '#07ECD7']);
    getMainDashboardData()

    $('#videos_dashboard').click(function () {
        getActiveCategory("videos_dashboard")
        loadVideoData(1);
    });

    $('#users_dashboard').click(function () {
       getActiveCategory("users_dashboard")
        loadUserData(1);
    });

    $('#home_dashboard').click(function () {
        getActiveCategory("home_dashboard");
    });

    function setPreviousText() {
        previousText = document.getElementById("search").value;
    }

    function Search(pageNumber) {
        var searchKey = previousText;
        if(searchKey == "") {
            if(table.classList.contains('user_table')) {
                loadUserData(1);
            }
            else {
                loadVideoData(1);
            }
        }
        else{
        if(table.classList.contains('user_table')) {   
                $.ajax({
                    url: 'search_users/page=' + pageNumber, // Replace with your API endpoint URL
                    method: 'GET',
                    data: { 'email': searchKey},
                    success: function(data) {
                        table.classList.add('search_table')
                        $('#data_table tbody').empty();
                        currentPageElement.innerHTML = pageNumber;
                        $('#current_page_number').html(pageNumber);
                        $('#total_pages').html(data.num_pages);
                        if(data.results.length == 0 || data.num_pages == 1){
                            nextButton.classList.add('hidden');
                            currentPageElement.classList.add('hidden');
                            if(data.results.length == 0) {
                                titlePage.classList.add('hidden');
                                titleOf.classList.add('hidden');
                                totalPagesElement.classList.add('hidden');
                                currentPageNumberElement.classList.add('hidden');
                                resultsNumber.innerHTML = "No users found";
                            }
                            else {
                                titlePage.classList.remove('hidden');
                                titleOf.classList.remove('hidden');
                                totalPagesElement.classList.remove('hidden');
                                currentPageNumberElement.classList.remove('hidden');
                                resultsNumber.innerHTML = "Results: " + data.count;
                            }
                        } else {
                            nextButton.classList.remove('hidden');
                            currentPageElement.classList.remove('hidden');
                            titlePage.classList.remove('hidden');
                            titleOf.classList.remove('hidden');
                            totalPagesElement.classList.remove('hidden');
                            currentPageNumberElement.classList.remove('hidden');
                            resultsNumber.innerHTML = "Results: " + data.count;
                        }
                        if(pageNumber == 1)
                        previousButton.classList.add('hidden')
                        if(pageNumber == data.num_pages)
                        { nextButton.classList.add('hidden'); }
                        // Display search results in the 'searchResults' div
                        $.each(data.results, function (index, user) {
                            // Determine the button color based on the user's status
                            var statusColor = user.status == 'banned' ? 'rose-500' : 'green-500';
                            var buttonColor = user.status == 'banned' ? 'blue' : 'red';
                            var buttonContent = user.status == 'banned' ? '<i class="fa-solid fa-unlock"></i>' : '<i class="fa-solid fa-ban"></i>';
                            var row = '<tr class="text-center h-14" data-user-id="' + user.id + '">' +
                                '<td class="px-4 py-2 border text-center">' + user.id + '</td>' +
                                '<td class="px-4 py-2 border text-center">' + user.email + '</td>' +
                                '<td class="px-4 py-2 border text-center">' + '<h4 class="w-3/6 min-w-min rounded border text-stroke text-white font-medium bg-' + statusColor + ' inline-block">' + capitalizeFirstLetter(user.status) +'<h4></td>' +
                                '<td class="px-4 py-2 border text-center">' +
                                    '<button class="w-18 h-18 rounded-lg bg-' + buttonColor + '-500 text-white py-1 px-3 rounded-full" onclick="banUser(' + user.id + ')" ' +
                                     ' id="' + user.id + '">'+ buttonContent + '</button>' +
                                '</td>'+
                                '</tr>';
                            $('#data_table tbody').append(row);
                        });       
                    },
                    error: function() {
                        alert('Failed to fetch search results.');
                    }
                });
        }
        else {
            $.ajax({
                url: 'search_videos/page=' + pageNumber,  
                method: 'GET',
                data: { 'query': searchKey },
                success: function (data) {
                    table.classList.add('search_table')
                    $('#data_table tbody').empty();
                    currentPageElement.innerHTML = pageNumber;
                    $('#current_page_number').html(pageNumber);
                    $('#total_pages').html(data.num_pages); 
                    if(data.results.length == 0 || data.num_pages == 1){
                        nextButton.classList.add('hidden');
                        currentPageElement.classList.add('hidden');
                        if(data.results.length == 0) {
                            titlePage.classList.add('hidden');
                            titleOf.classList.add('hidden');
                            totalPagesElement.classList.add('hidden');
                            currentPageNumberElement.classList.add('hidden');
                            resultsNumber.innerHTML = "No videos found";
                        }
                        else {
                            titlePage.classList.remove('hidden');
                            titleOf.classList.remove('hidden');
                            totalPagesElement.classList.remove('hidden');
                            currentPageNumberElement.classList.remove('hidden');
                            resultsNumber.innerHTML = "Results: " + data.count;
                        }
                    } else {
                        nextButton.classList.remove('hidden');
                        currentPageElement.classList.remove('hidden');
                        titlePage.classList.remove('hidden');
                        titleOf.classList.remove('hidden');
                        totalPagesElement.classList.remove('hidden');
                        currentPageNumberElement.classList.remove('hidden');
                        resultsNumber.innerHTML = "Results: " + data.count;
                    }
                    if(pageNumber == 1)
                    previousButton.classList.add('hidden')
                    if(pageNumber == data.num_pages)
                    { nextButton.classList.add('hidden'); }
                    $.each(data.results, function (index, video) {
                        var videoStatusColor
                        var customDate = formatCustomDate(video.created_at);
                        if(video.status == 'pending')
                            videoStatusColor = 'yellow-500'
                        else if(video.status == 'completed')
                            videoStatusColor = 'green-500'
                        else
                            videoStatusColor = 'rose-500'
                        var row = '<tr class="text-center h-14">' +
                            '<td class="px-4 py-2 border text-center">' + video.id + '</td>' +
                            '<td class="px-4 py-2 border text-center">' + video.user_id + '</td>' +
                            '<td class="px-4 py-2 border text-center">' + '<h4 class="w-4/5 min-w-min rounded border text-stroke text-white font-medium bg-' + videoStatusColor + ' inline-block">' + capitalizeFirstLetter(video.status) +'<h4></td>' +
                            '<td class="px-4 py-2 border text-center">' + customDate + '</td>' +
                            '<td class="px-4 py-2 border text-left truncate hover:text-clip">' + video.original_video_path+ '</td>' +
                            '</tr>';
                        $('#data_table tbody').append(row);
                    });
                },
                error: function () {
                    console.log('API request for videos failed');
                }
            });
        }}
    };

    $(`#search_button`).click(function () {
        setPreviousText()
        Search(1)
    });

    function getNewPage(type) {
        var totalPages = parseInt(totalPagesElement.innerHTML);
        var pageNumber
        if(type == "Next"){
            pageNumber = parseInt(currentPageElement.innerHTML) + 1;
            if (pageNumber == totalPages) { nextButton.classList.add('hidden') };
            if (pageNumber > 1) { previousButton.classList.remove('hidden') }
        }
        else {
            pageNumber = parseInt(currentPageElement.innerHTML) - 1;
            if(pageNumber == 1){ previousButton.classList.add('hidden') } }; 
            if (pageNumber < totalPages) { nextButton.classList.remove('hidden') };

        currentPageElement.innerHTML = pageNumber;
        if (table.classList.contains('search_table')) {
                Search(pageNumber); 
        }
        else {
            if (table.classList.contains('user_table')) {
                loadUserData(pageNumber); 
            }
            else {
                loadVideoData(pageNumber);
            }
        }
    }
    
   $(`#next_button`).click(function () {
    getNewPage("Next")
    });

    $(`#previous_button`).click(function () {
        getNewPage("Previous")
    });
    });
function banUser(userId) {
        // Make an AJAX request to your API to change the user's status to "Banned"
        $.ajax({
            url: 'users/' + userId + '/ban/',  // Replace with your API endpoint URL
            method: 'PUT',  // Use the appropriate HTTP method (PUT or PATCH) for your API
            success: function (data) {
                // Update the user's status in the table
                const statusCell = document.querySelector(`#data_table tbody tr[data-user-id="${userId}"] td:nth-child(3) h4`);
                if(statusCell.textContent =='Active')
                {statusCell.textContent = 'Banned';
                statusCell.classList.remove('bg-green-500');
                statusCell.classList.add('bg-red-500');
                }
                else {statusCell.textContent = 'Active';
                statusCell.classList.remove('bg-red-500');
                statusCell.classList.add('bg-green-500');
                }
                const button = document.querySelector(`#data_table tbody tr[data-user-id="${userId}"] td:nth-child(4) button`);
                if(statusCell.textContent =='Banned')
                {
                button.classList.remove('bg-red-500');
                button.classList.add('bg-blue-500');
                button.innerHTML = '<i class="fa-solid fa-unlock"></i>';
                }
                else {
                    button.classList.remove('bg-blue-500');
                    button.classList.add('bg-red-500');
                    button.innerHTML = '<i class="fa-solid fa-ban"></i>';
                }
            },
            error: function () {
                alert('Failed to ban the user. Please try again later.');
            }
        });
    };
    
    function consoleText(words, id, colors) {
        if (colors === undefined) colors = ['#fff'];
        var visible = true;
        var con = document.querySelector(`#console`);
        var letterCount = 1;
        var x = 1;
        var waiting = false;
        var target = document.getElementById(id);
        target.setAttribute('style', 'color:' + colors[0])
        window.setInterval(function() {
          if (letterCount === 0 && waiting === false) {
            waiting = true;
            target.innerHTML = words[0].substring(0, letterCount)
            window.setTimeout(function() {
              var usedColor = colors.shift();
              colors.push(usedColor);
              var usedWord = words.shift();
              words.push(usedWord);
              x = 1;
              target.setAttribute('style', 'color:' + colors[0])
              letterCount += x;
              waiting = false;
            }, 1000)
          } else if (letterCount === words[0].length + 1 && waiting === false) {
            waiting = true;
            window.setTimeout(function() {
              x = -1;
              letterCount += x;
              waiting = false;
            }, 1000)
          } else if (waiting === false) {
            target.innerHTML = words[0].substring(0, letterCount)
            letterCount += x;
          }
        }, 120)
        window.setInterval(function() {
          if (visible === true) {
            con.classList.add('hidden')
            visible = false;
          } else {
            con.classList.remove('hidden');
            visible = true;
          }
        }, 400)
      };
