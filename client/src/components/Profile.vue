<template>
    <div id="Profile" class="container">
        <form @submit.prevent="submitProfile">
            <img id="preview" src="/static/profile.png" width="120px" height="120px"/>
            <br>
            <h6>Upload Your profile pic:</h6>
            <input id="pop_file" type="file" accept=".jpg,.jpeg,.png" v-on:change="uploadFile($event)" name="fileTrans" ref="file" value=""/>
            <br><br> Gender: <br>
            <input type="radio" name="gender" value="male" v-model="gender"> Male
            <span id="c"><input type="radio" name="gender" value="female">Female</span>
            <span id="c"><input type="radio" name="gender" value="other"> Other</span>
            <br><br>
            Age:<br>
            <input type="number" name="age" value="20" v-model="age">
            <br><br>Constallation:
            <!-- <br><input list="constellations" name="constellation" v-model="constellation">
            <datalist id="constellations">
                <option value="Auqarius"></option>
                <option value="Sagittarius"></option>
                <option value="Pisces"></option>
                <option value="Gemini"></option>
                <option value="Aries"></option>
                <option value="Cancer"></option>
                <option value="Leo"></option>
                <option value="Libra"></option>
                <option value="Taurus"></option>
                <option value="Virgo"></option>
                <option value="Scorpio"></option>
                <option value="Capricorn"></option>
            </datalist> -->
            <br><br>Birthday:
            <br><input type="date" name="birth" value="" v-model="birth">
            <br><br>Location:
            <br><input type="text" name="location" value="" v-model="location">
            <h6>Set Your Personalized Signature: </h6>
            <textarea cols="20" rows="6" v-model="signature"></textarea>
            <br><br>
            <button id="c" type="submit" value="Submit">Submit</button>
        </form>
        <h3> {{ status }} </h3>
        <router-link style="text-align:center" to="/">
        <a>Home Page</a>
        </router-link>
        <div>
        <button>Log Out</button>
        </div>
    </div>
</template>

<script>
import { Logger } from "@/common"

const logger = Logger.get("actions.js")

export default {
    name: 'Profile',

    data () {
        return {
            title: 'Profile',
            // pic: '',
            gender: '',
            age: '',
            birth: '',
            constellation: '',
            location: '',
            signature: '',
            status: 'Edit Your Profile'
        }
    },
    computed: {
    },
    methods: {
        uploadPhoto () {
            let dataURl = ''
            const file = document.getElementById('pop_file')
            const fileObj = file.files[0]
            const windowURL = window.URL || window.webkitURL
            const img = document.getElementById('preview')
            if (file && fileObj) {
                dataURl = windowURL.createObjectURL(fileObj)
                img.setAttribute('src', dataURl)
                console.log("upload profile pic" + dataURl)
            }
            this.$store
                .dispatch("uploadPic", {
                    path: dataURl
                })
                .then(
                    (json) => {
                        if (json.available) {
                            this.message = "Path Available"
                        } else {
                            this.message = "Path Isn't Available"
                        }
                    }, err => {
                        this.message = " failed: " + err
                    }
                )
        },
        submitProfile () {
            console.log("submitProfile")
            this.$store
                .dispatch("submitProfile", {
                    // pic: this.pic,
                    gender: this.gender,
                    age: this.age,
                    birth: this.birth,
                    constellation: this.constellation,
                    location: this.location,
                    signature: this.signature
                })

                .then(
                    () => {
                        this.status = "Saved !!!"
                    },
                    err => {
                        this.c2 = "color:tomato"
                        this.status = "Unsaved, try later " + err
                    }
                )
        }
    }
}
</script>

<style scoped>
.container {
  width: 700px;
  height: 700px;
}

#c,h6{
    color:rgb(50, 122, 204)
}

div{
    margin-top:10px;
}

a{
    color:coral;
}

form {
    position: absolute;
    margin-top: 0px;
    margin-right: 50px;
    color:rgb(50, 122, 204);
}

</style>
