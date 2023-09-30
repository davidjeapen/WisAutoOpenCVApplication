Here is the result of my solution:
![alt text][result]

[result]: ./answer.png "anser"

# Methodology

1. Create a mask of the image with only pixels that match the orange of the cones
   2. Logic courtesy of [Computer vision engineer](https://github.com/computervisioneng/color-detection-opencv)
2. Uses OpenCV findContours() on the mask to create a list of regions which contain cones
3. Splits screen into halves and saves the position of each of cone in an array
4. Uses scipy stats linregress() to take a linear regression of each lines of cones
5. Overlays each line on [red.png](./red.png) and exports result to [answer.png](./answer.png)

# Process
I initially tried to use a Haar Cascade model to detect the cone, but I was unable to find a model in a reasonable
amount of time and did not have enough sample images or time to train a model myself. Then I found a Computer vision
engineer video which I used a model to detect the cones by color. I had to fine tune the color orange and range I was
looking for but was able to find a range of color which detected the cones.
Then I had to find a way to turn the color mask into individual cones.
After a bit of seaching, I discovered the findContours method which took in the mask and exported a list of regions 
(which were cones)
I was then able to draw boxes around each of these regions to see what cones were being detected.
Then I found a way to take the linear regression of points using the scipy stats library which allowed my to get the
equation for a line which best passed through the cones on either side of the screen.
Next I was able to draw lines through the cones.
However, the lines I drew used the equation from the regression model with the x values from the cone positions
so the lines only went through the cones and did not go past them in both directions like the desired output.
Instead of used the corners of the image as the x values to graph the line allowing the lines to show the full path
before and after the cones.
Then I figured out how to export the matplotlib output I was using to an image using savefig() and formated the output
image so it would have the original dimensions and not as much white margin.

# Libraries Used

  - [OpenCV](https://pypi.org/project/opencv-python/)
  - [scipy](https://scipy.org)
  - [matplotlib](https://matplotlib.org)
  - [numpy](https://numpy.org)