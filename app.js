const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const cookieParser = require("cookie-parser");
const app = express();

const fs = require("fs"); // Require the Node.js file system module
app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static("public"));
app.use(cookieParser());
app.use(express.json());
// app.use(express.urlencoded({ extended: true }));
// app.use(express.static(path.join(__dirname, "public")));
mongoose
  .connect("mongodb://127.0.0.1:27017/carrer_db", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("MongoDB connected"))
  .catch((err) => console.log(err));

const User = require("./models/user");

// Middleware to verify JWT
const authenticateToken = (req, res, next) => {
  const token = req.cookies.jwt;
  if (token == null) return res.sendStatus(401);
  jwt.verify(token, "secretkey", (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
};

app.get("/", (req, res) => {
  res.render("index");
});

app.get("/login", (req, res) => {
  res.render("login");
});

app.get("/signup", (req, res) => {
  res.render("signup");
});

app.post("/sign_up", async (req, res) => {
  const { name, email, password1, password2 } = req.body;
  console.log(req.body);
  try {
    const hashedPassword = await bcrypt.hash(password1, 10);
    const user = new User({ name, email, password: hashedPassword });
    await user.save();
    res.redirect("/login");
  } catch {
    res.redirect("/signup");
  }
});

app.post("/login", async (req, res) => {
  const { name, password } = req.body;
  console.log(req.body);
  const user = await User.findOne({ name });
  if (user == null) {
    return res.status(400).send("Cannot find user");
  }
  try {
    if (await bcrypt.compare(password, user.password)) {
      const accessToken = jwt.sign(
        { name: user.name, email: user.email },
        "secretkey"
      );
      res.cookie("jwt", accessToken, { httpOnly: true });
      res.render("home");
    } else {
      res.send("Not Allowed");
    }
  } catch {
    res.status(500).send();
  }
});

app.get("/low", (req, res) => {
  res.render("low");
});
app.get("/mid", (req, res) => {
  res.render("low");
});
app.get("/high", (req, res) => {
  res.render("low");
});

// app.post("/lowsubmit", (req, res) => {
//   console.log(req.body);
//   res.render("low");
// });

app.get("/logout", (req, res) => {
  res.clearCookie("jwt");
  res.redirect("/");
});

app.post("/lowsubmit", (req, res) => {
  // Log the req.body to console
  console.log(req.body);

  // Convert req.body to JSON string
  const jsonData = JSON.stringify(req.body, null, 2); // null and 2 for pretty formatting

  // Write JSON string to a file (e.g., data.json)
  fs.writeFile("student_data1.json", jsonData, "utf8", (err) => {
    if (err) {
      console.error("Error writing JSON file:", err);
      return res.status(500).send("Error saving data");
    }
    console.log("JSON file has been saved");
    // Render your 'low' template or send a response
    res.render("low");
  });
  const fs = require("fs");

  // Read the JSON file
  fs.readFile("student_data1.json", "utf8", (err, data) => {
    if (err) {
      console.error(err);
      return;
    }

    data = JSON.parse(data);

    // Format the data
    const formatted_data = {
      personal_data: {
        name: data["personal_data[name]"],
        age: parseInt(data["personal_data[age]"], 10),
        gender: data["personal_data[gender]"],
      },
      interests: [...new Set(data["interests[]"])],
      skills: Object.fromEntries(
        Object.entries(data)
          .filter(([key, value]) => key.startsWith("skills[") && value)
          .map(([key, value]) => [key.slice(7, -1), parseInt(value, 10)])
      ),
      your_location: data["your_location"],
      economical_status: data["economical_status"],
      subjects: {
        literature: data["subjects[literature]"],
        physics: data["subjects[physics]"],
        chemistry: data["subjects[chemistry]"],
        mathematics: data["subjects[mathematics]"],
        languages: data["subjects[languages]"],
        biology: data["subjects[biology]"],
        sports: data["subjects[sports]"],
      },
      peer_interests: [...new Set(data["interests[]"])],
      mindset: {
        decision_making_style: data["mindset[decision_making_style]"],
        career_expectations: data["mindset[career_expectations]"],
      },
      reqd: parseInt(data["reqd"], 10),
    };

    // Write the formatted data back to the JSON file
    fs.writeFile(
      "student_data1.json",
      JSON.stringify(formatted_data, null, 4),
      "utf8",
      (err) => {
        if (err) {
          console.error(err);
        } else {
          console.log("Data successfully written to student_data1.json");
        }
      }
    );
  });
});

app.get("/protected", authenticateToken, (req, res) => {
  res.send(
    '<h1>This is a protected route</h1><img src="/images/protected-image.jpg" alt="Protected Image">'
  );
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
