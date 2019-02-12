<template>
    <div id="Profile" class="container" @submit.prevent="userProfile">
        <div class="b">
            <img id="preview" src="/static/profile.png" width="120px" height="120px"/>
            <br>
            <h6>Upload Your profile pic:</h6>
            <input id="pop_file" type="file" accept=".jpg,.jpeg,.png" v-on:change="uploadFile($event)" name="fileTrans" ref="file" value=""/>
        </div>
        <form>
            Gender:<br>
            <input type="radio" name="gender" value="male"> Male
            <span id="c"><input type="radio" name="gender" value="female">Female</span>
            <span id="c"><input type="radio" name="gender" value="other"> Other</span>
            <br><br>
            Age:<br>
            <input type="number" name="age" value="20">
            <br><br>Constallation:
            <br><input list="constellations" name="constellation">
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
            </datalist>

            <br><br>Birthday:
            <br><input type="date" name="birth" value="">
            <br><br>Location:
            <br><input type="text" name="location" value="">
            <h6>Set Your Personalized Signature: </h6>
            <textarea cols="20" rows="6"></textarea>
            <br><br>
            <button id="c" type="submit" value="Submit">Submit</button>
            <span>
            <router-link style="text-align:center" to="/">
            <a>Home Page</a>
            </router-link>
            </span>
        </form>
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
        }
    },
    computed: {
    },
    methods: {
        uploadFile () {
            const file = document.getElementById('pop_file')
            const fileObj = file.files[0]
            const windowURL = window.URL || window.webkitURL
            const img = document.getElementById('preview')
            if (file && fileObj) {
                const dataURl = windowURL.createObjectURL(fileObj)
                img.setAttribute('src', dataURl)
            }
            console.log("upload profile pic" + dataURl)
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
    }
}
</script>

<style scoped>
.container {
  width: 600px;
  height: 500px;
}

#c,h6{
    color:rgb(50, 122, 204)
}

.b{
    position: absolute;
    margin-top:0px;
    margin-right: 120px;
    color: rgb(50, 122, 204)
}

form {
    position: absolute;
    margin-top: 0px;
    margin-right: 50px;
    color:rgb(50, 122, 204);
}

</style>
