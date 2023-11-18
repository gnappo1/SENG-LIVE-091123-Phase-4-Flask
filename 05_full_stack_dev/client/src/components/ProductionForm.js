import React, {useState} from 'react'
import styled from 'styled-components'
import { useHistory } from 'react-router-dom'
// 6.✅ Verify formik and yet have been added to our package.json dependencies 
import { Formik } from 'formik';
import * as yup from 'yup';



function ProductionForm({addProduction, handleNewError}) {

  const history = useHistory()
  // 7.✅ Use yup to create client side validations
 const productionSchema = yup.object().shape({
  title: yup.string()
    .min(2, "Titles must be at least 2 chars long")
    .max(50, "Titles must be 50 chars long max")
    .required("Title is required"),
  genre: yup.string()
    .oneOf(["Drama", "Musical", "Opera"])
    .required("Genre has to be one of Drama, Musical, Opera"),
  budget: yup.number()
    .positive("Budget has to be a positive integer")
    .max(10000000, "Budget must be 50 chars long max")
    .required("Budget has to be a positive float under 10Millions"),
  image: yup.string()
    .test("is-url", "Images must have a valid url ending with jpg, jpeg, png", (value) => {
        const urlRegex = /(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|jpeg|png)/g;
        return urlRegex.test(value)
    })
    .required("Image is required"),
  director: yup.string()
    .required("Director is required"),
  description: yup.string()
    .min(30, "Description should be at least 10 chars")
    .max(500, "Description should be 10000 chars max")
    .required("Description is required")
 })


  // 9.✅ useFormik hook
    return (
      <div className='App'>
        <Formik
          initialValues={{ title: '', genre: '', budget: '', image: '', director: '', description: '', ongoing: '' }}
          validationSchema={productionSchema}
          onSubmit={(values) => {
            fetch("/productions", {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify({...values, ongoing: true})
            })
            .then(resp => {
              if (resp.ok) { //! 201
                resp.json().then((newProduction) => {
                  addProduction(newProduction)
                  history.push("/")
                })
              } else {
                resp.json().then(errorObj =>handleNewError(errorObj.message))
              }
            })
            .catch(errorObj =>handleNewError(errorObj.message))
          }}
        >
          {({
            values,
            errors,
            touched,
            handleChange,
            handleBlur,
            handleSubmit,
            isSubmitting,
            /* and other goodies */
          }) => (
            <Form onSubmit={handleSubmit}>
            <label>Title </label>
            <input type='text' name='title' onChange={handleChange} onBlur={handleBlur} value={values.title}/>
            {errors.title && touched.title ? <div className="error-message show">{errors.title}</div> : null}
            <label> Genre</label>
            <input type='text' name='genre' onChange={handleChange} onBlur={handleBlur} value={values.genre}/>
            {errors.genre && touched.genre ? <div className="error-message show">{errors.genre}</div> : null}

            <label>Budget</label>
            <input type='number' name='budget' onChange={handleChange} onBlur={handleBlur} value={values.budget}/>
            {errors.budget && touched.budget ? <div className="error-message show">{errors.budget}</div> : null}
            <label>Image</label>
            <input type='text' name='image'  onChange={handleChange} onBlur={handleBlur} value={values.image}/>
            {errors.image && touched.image ? <div className="error-message show">{errors.image}</div> : null}
            <label>Director</label>
            <input type='text' name='director' onChange={handleChange} onBlur={handleBlur} value={values.director}/>
            {errors.director && touched.director ? <div className="error-message show">{errors.director}</div> : null}
            <label>Description</label>
            <textarea type='text' rows='4' cols='50' name='description' onChange={handleChange} onBlur={handleBlur} value={values.description} />
            {errors.description && touched.description ? <div className="error-message show">{errors.description}</div> : null}
            <input type='submit' disabled={isSubmitting}/>
          </Form> 
          )}
      </Formik>
      
      </div>
    )
  }
  
  export default ProductionForm

  const Form = styled.form`
    display:flex;
    flex-direction:column;
    width: 400px;
    margin:auto;
    font-family:Arial;
    font-size:30px;
    input[type=submit]{
      background-color:#42ddf5;
      color: white;
      height:40px;
      font-family:Arial;
      font-size:30px;
      margin-top:10px;
      margin-bottom:10px;
    }
  `