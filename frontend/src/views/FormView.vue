<script setup>
import { ref } from 'vue';

const formData = ref({
  name: '',
  email: '',
  age: null,
});

const successMessage = ref('');
const errorMessage = ref('');

const handleSubmit = async () => {

    try {
      const response = await sendFormDataToBackend(formData.value);

      // Handle success response
      if (response.success) {
        successMessage.value = 'Form submitted successfully!';
        resetForm();
      } else {
        // Handle failure response
        errorMessage.value = 'Form submission failed. Please check the following fields:';
        // Display the specific fields that failed
        errorMessage.value += response.failedFields.join(', ');
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      errorMessage.value = 'An error occurred while submitting the form.';
    }
};

const resetForm = () => {
  formData.value = {
    name: '',
    email: '',
    age: null,
  };
};


const sendFormDataToBackend = async (formData) => {
  // Simulate sending data to the backend and getting a response
  return new Promise((resolve) => {
    setTimeout(() => {
      // Simulate a successful response
      // Replace this with actual API call in a real application
      resolve({
        success: true,
      });

      // Simulate a failure response
      // Uncomment the following lines to simulate a failure
      // resolve({
      //   success: false,
      //   failedFields: ['name', 'email'],
      // });
    }, 1000);
  });
};
</script>

<template>
  <div class="center-box">
    <div class="form-box">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="formData.name" placeholder="Name & Surname" required />
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="tex" id="email" v-model="formData.email" required />
        </div>
        <div class="form-group">
          <label for="age">Age:</label>
          <input type="text" id="age" v-model="formData.age" required />
        </div>
        <button type="submit">Submit</button>
      </form>

      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.center-box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.form-box {
  width: 300px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>