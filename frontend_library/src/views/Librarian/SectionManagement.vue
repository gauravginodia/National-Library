<template>
  <div>
  <NavBar/>
  <div class="container">
    <div class="dropdown">
  <button class="btn btn-primary dropdown-toggle" type="button" id="dropdownMenuButton"  @click="toggleDropdown">
    Add Section
  </button>
  <div class="dropdown-menu"  :class="{ 'show': isDropdownOpen }" aria-labelledby="dropdownMenuButton">
    <div class="card text-center bg-dark text-white">
      <div class="card-body">
        <h5 class="card-title">Add Section</h5>
        <hr class="bg-white" />
        <form @submit.prevent="addSection">
          <div class="form-group">
            <label for="name">Section Name:</label>
            <input type="text" class="form-control" id="name" v-model="newSection.name" required>
          </div>
          <div class="form-group">
            <label for="date">Date:</label>
            <input type="date" class="form-control" id="date" v-model="newSection.date" required>
          </div>
          <div class="form-group">
            <label for="description">Description:</label>
            <textarea class="form-control" id="description" v-model="newSection.description"></textarea>
          </div>
          <button type="submit" class="btn btn-success" @click="toggleDropdown">Save</button>
        </form>
      </div>
    </div>
  </div>
</div>

    
    <input style="width:100%;padding: 0.5%;border-width:0.5cap;border-radius: 10cqb; color:black;font-weight: 700;font-size:large;text-align: center;border-color: black;margin-bottom:2%;margin-top: 3%;" type="text" v-model="searchBar" placeholder="Type a section name to search">


    <div class="flip-card" v-for="section in searchSections" :key="section.id">
      <div class="flip-card-inner" :class="{ flipped: section.flipped }" @click="flipCard(section.id)">
        <div class="flip-card-front" :style="{ background: 'linear-gradient(to right, #434343 0%, black 100%)'}">
          <h3 style="color:white;justify-content: center;margin-top:25%">{{ section.name }}</h3>
          <p>{{ section.date }}</p>
        </div>
        <div class="flip-card-back" :style="{background: 'linear-gradient(147deg, #c3cbdc 0%, #edf1f4 74%)'}">

          <router-link :to="'/librarian/dashboard/section/' + section.id + '/' + section.name" class="view-button">View</router-link>
          <button class="delete-button" @click="deleteSection(section.id)">Delete</button>
        </div>
      </div>
    </div>

  </div>
</div>
</template>

<script>
import NavBar from "../../components/NavBar.vue";
import axios from "axios";

export default {
  name: "SectionManagement",
  components: {
    NavBar,
  },
  mounted() {
    this.getSections();
    // this.toggleDropdown();
  },
  data() {
    return {
      searchBar: "",
      sections: [], // Replace with your actual data
      showAddModal: false,
      newSection: {
        name: "",
        date: "",
        description: "",
      },
      isDropdownOpen: false,
    };
  },

  methods: {
    flipCard(id) {
      const sectionIndex = this.sections.findIndex((section) => section.id === id);
      this.sections[sectionIndex].flipped = !this.sections[sectionIndex].flipped;
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    
    getSections() {
      const headers = new Headers();
      headers.append('Authorization', `Bearer ${localStorage.getItem("accessToken")}`);

      fetch("http://127.0.0.1:5000/api/sections", {
        method: 'GET',
        headers: headers,
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          this.sections = data.map(section => ({
            ...section,
            color1: this.getRandomColor(),
            color2: this.getRandomColor()
          }));
          console.log(this.sections);
        })
        .catch(error => {
          console.error('Error fetching sections:', error);
        });
    },
 
    deleteSection(id) {
      axios.delete(`http://127.0.0.1:5000/api/delete/section/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      })
        .then((response) => {
          console.log("Section removed successfully.", response.data);
          // Remove the section from the local array
          this.sections = this.sections.filter(section => section.id !== id);
          alert(response.data.message);
        })
        .catch((error) => {
          console.error("Error removing section:", error);
        });
    },
    openModal() {
      this.showAddModal = true;
      this.newSection = { name: "", date: "", description: "" }; 
    },
    closeModal() {
      this.showAddModal = false;
    },
    addSection() {
      axios.post("http://127.0.0.1:5000/api/add/new-section", this.newSection, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      })
        .then((response) => {
          console.log("Section added successfully.", response.data);
          this.newSection = {
            title: "",
            date: "",
            description: "",
          };
          location.reload();
          alert(response.data.message);
        })
        .catch((error) => {
          console.error("Error adding section:", error);
        });
      const randomColor1 = this.getRandomColor();
      const randomColor2 = this.getRandomColor();
      this.sections.push({ ...this.newSection, id: Math.random(), color1: randomColor1, color2: randomColor2 }); // Simulate ID generation
      this.closeModal();
    },
    getRandomColor() {
      const colors = ["#FF5733", "#FFBD33", "#33FF57", "#337DFF", "#AB33FF"]; // Add more colors as needed
      return colors[Math.floor(Math.random() * colors.length)];
    },
  },
  computed: {
    searchSections() {
      return this.sections.filter(section =>
        section.name.toLowerCase().includes(this.searchBar.toLowerCase())
      );
    }
  },
};
</script>

<style scoped>
.card.text-center.mt-4.bg-dark {
  border: 1px solid #333;
  border-radius: 0.5rem;
}

.card-title, .card-text {
  color: #fff;
}

.field {
  margin-bottom: 1rem;
}

.label {
  color: #fff;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.input,
.textarea {
  background-color: white;
  border: 1px solid #444;
  border-radius: 0.25rem;
  color: green;
  font-weight: bold;
  padding: 0.5rem;
  width: 100%;
}

.textarea {
  resize: vertical;
  min-height: 100px;
}

.btn-success {
  background-color: transparent;
  border:#fff;
  color: #fff;
  cursor: pointer;
}

.btn-success:hover {
  background-color: #1e7c31;
}

.form {
  background:rgba(#13232f,.9);
  padding: 20px;
  max-width:600px;
  border-radius:4px;
  box-shadow:0 4px 10px 4px rgba(#13232f,.3);
}
.container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  padding: 20px;
}

.add-section {
  margin-bottom: 20px;
}

.flip-card {
  background-color: transparent;
  width: 300px;
  height: 200px;
  border: 1px solid #f1f1f1;
  perspective: 1000px; /* Remove this if you don't want the 3D effect */
}

/* This container is needed to position the front and back side */
.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.8s;
  transform-style: preserve-3d;
}

.flip-card:hover .flip-card-inner {
  transform: rotateY(180deg);
}

.flip-card-front, .flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  -webkit-backface-visibility: hidden; 
  backface-visibility: hidden;
}

.flip-card-front {
  color: black;
}

/* Style the back side */
.flip-card-back {
  color: white;
  transform: rotateY(180deg);
}

.view-button, .delete-button {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin-top:25%;
  margin-right: 4px;
  cursor: pointer;
  border-radius: 5px;
}

.view-button:hover, .delete-button:hover {
  background-color: #45a049; /* Darker Green */
}

.card-front,
.card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  border-radius: 5px;
}

/* Style for the modal */
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  width: 400px;
  padding: 20px;
  border-radius: 5px;
  /* Custom styles */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}


/* Style for buttons inside the modal */
.modal button {
  /* Common button styles */
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
}

/* Style for submit button */
.modal button[type="submit"] {
  background-color: #4CAF50; /* Green */
  color: white;
}

/* Style for cancel button */
.modal button[type="button"] {
  background-color: #f44336; /* Red */
  color: white;
}

/* Hover styles for buttons */
.modal button:hover {
  opacity: 0.8;
}

/* Style for input fields */
.modal input[type="text"],
.modal input[type="date"],
.modal textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

/* Additional styles for specific form elements if needed */

</style>
