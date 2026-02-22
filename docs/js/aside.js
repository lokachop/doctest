entry = document.getElementById("sidebar-search");
container = document.getElementById("aside-container");
aside = document.getElementById("aside");


var defs;
fetch("js/defs.json").then((res) => res.text()).then((text) => {
	defs = JSON.parse(text);

	var searchQuery = sessionStorage.getItem("searchQuery");
	if(searchQuery != null) {
		recomputeAside(searchQuery);
		entry.value = searchQuery;
	} else {
		recomputeAside("");
	}


	var scrollKeep = sessionStorage.getItem("scrollKeep");
	if(scrollKeep != null) {
		aside.scrollTop = scrollKeep;
	}
}).catch((e) => console.error(e));

function recomputeAside(search) {
	search = search.toLowerCase();
	container.innerHTML = "";

	matchingEntries = {};

	for (i = 0; i < defs.length; i++) {
		var entry = defs[i];
		var loneSig = entry["lonesig"].toLowerCase();

		if (loneSig == null) {
			continue;
		}

		var found = loneSig.search(search);
		if (found == -1) {
			continue;
		}

		var group = entry["group"];
		if (!matchingEntries[group]) {
			matchingEntries[group] = [];
		}
		var entryList = matchingEntries[group];

		var category = entry["category"];
		if (!entryList[category]) {
			entryList[category] = [];
		}

		entryList[category].push(entry);
	}

	var sortedGroups = Object.keys(matchingEntries).map(function (k) {
		return [k, matchingEntries[k]];
	})

	sortedGroups.sort(function (a, b) {
		if (a[0] < b[0]) {
			return -1;
		}

		if (a[0] > b[0]) {
			return 1;
		}
		return 0;
	});

	for (var i = 0; i < sortedGroups.length; i++) {
		// another stupid sub sort
		var groupTitle = sortedGroups[i][0];
		var groupCont = sortedGroups[i][1];
		var sortTwo = Object.keys(groupCont).map(function (k) {
			return [k, groupCont[k]];
		})

		sortTwo.sort(function (a, b) {
			if (a[0] < b[0]) {
				return -1;
			}

			if (a[0] > b[0]) {
				return 1;
			}
			return 0;
		});

		var header = document.createElement("li");
		header.setAttribute("class", "group-header");
		header.textContent = groupTitle;
		container.appendChild(header);

		var groupCont = document.createElement("div");
		groupCont.setAttribute("class", "group");
		container.appendChild(groupCont);
		for (var j = 0; j < sortTwo.length; j++) {
			var categoryTitle = sortTwo[j][0];
			var categoryCont = sortTwo[j][1];

			categoryCont.sort(function (a, b) {
				if (a["lonesig"] < b["lonesig"]) {
					return -1;
				}

				if (a["lonesig"] > b["lonesig"]) {
					return 1;
				}
				return 0;
			});

			var catCont = document.createElement("div");
			catCont.setAttribute("class", "category");
			groupCont.appendChild(catCont);

			var catTitle = document.createElement("li");
			catTitle.setAttribute("class", "category-header");
			catTitle.textContent = categoryTitle;
			catCont.appendChild(catTitle);

			var catUL = document.createElement("ul");
			catCont.appendChild(catUL);

			for (var k = 0; k < categoryCont.length; k++) {
				var func = categoryCont[k];

				var entryLi = document.createElement("li");
				entryLi.setAttribute("class", "function");


				var entryImg = document.createElement("img");
				entryImg.setAttribute("src", "/img/realm/" + func["realm"] + ".png")
				entryImg.setAttribute("class", "realm-aside");
				entryLi.append(entryImg);


				var entrySpan = document.createElement("a");
				entrySpan.setAttribute("href", "/subpage/" + groupTitle + "/" + categoryTitle + "/" + func["lonesig"] + ".html");
				entrySpan.textContent = func["lonesig"];
				entryLi.append(entrySpan);

				catUL.append(entryLi);
			}
		}
	}

}

entry.addEventListener("keyup", function(event) {
	var currSearchEntry = entry.value;

	sessionStorage.setItem("searchQuery", currSearchEntry);

	recomputeAside(currSearchEntry);
})

aside.addEventListener("scroll", function(event) {
	sessionStorage.setItem("scrollKeep", aside.scrollTop);
})