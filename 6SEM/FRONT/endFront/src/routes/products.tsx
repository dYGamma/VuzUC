import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";
import React from "react";

const Product = ({
  title,
  description,
  price,
  inStock,
  images,
}: {
  title: string;
  description: string;
  price: number;
  inStock: boolean;
  images: string[];
}) => {
  return (
    <div className="flex flex-row gap-[3rem]">
      <div className="flex flex-col rounded-lg shadow-lg  max-h-[800px] aspect-square">
        <div className="flex flex-col">
          <Carousel>
            <CarouselContent>
              {images.map((src, idx) => (
                <CarouselItem key={idx}>
                  <div className="p-1">
                    <Card>
                      <CardContent className="flex aspect-square items-center justify-center p-6">
                        <img
                          key={idx}
                          src={src}
                          alt={`${title} image ${idx}`}
                          height={250}
                          width={250}
                        />
                      </CardContent>
                    </Card>
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </div>
      </div>
      <div className="flex flex-col p-4">
        <div className="text-xl font-bold">{title}</div>
        <div className="text-sm text-gray-500">{description}</div>
        <div className="text-sm font-semibold">${price}</div>
        {inStock && <div className="text-green-500">In stock</div>}
        {!inStock && <div className="text-red-500">Out of stock</div>}
      </div>
    </div>
  );
};

const ProductsPage = () => {
  const products = [
    {
      title: "Vivo Phone",
      description: "Modern phone with high-quality camera and fast performance",
      price: 1000,
      inStock: true,
      images: ["/vivo-1.jpg", "/vivo-2.jpg", "/vivo-3.jpg"],
    },
    {
      title: "Product 2",
      description: "Modern phone with high-quality camera and fast performance",
      price: 2000,
      inStock: false,
      images: [
        "https://picsum.photos/200/300",
        "https://picsum.photos/200/300",
        "https://picsum.photos/200/300",
        "https://picsum.photos/200/300",
      ],
    },
    {
      title: "Product 3",
      description: "Modern phone with high-quality camera and fast performance",
      price: 1500,
      inStock: true,
      images: [
        "https://picsum.photos/200/300",
        "https://picsum.photos/200/300",
        "https://picsum.photos/200/300",
      ],
    },
    {
      title: "Product 4",
      description: "Modern phone with high-quality camera and fast performance",
      price: 800,
      inStock: true,
      images: [
        "https://picsum.photos/200/300",
        "https://picsum.photos/200/300",
        "https://picsum.photos/200/300",
      ],
    },
    {
      title: "Product 5",
      description: "Modern phone with high-quality camera and fast performance",
      price: 10,
      inStock: true,
      images: [
        "https://picsum.photos/200/300",
        "https://picsum.photos/200/300",
        "https://picsum.photos/200/300",
      ],
    },
  ];

  const [currentProductIndex, setCurrentProductIndex] = React.useState(0);

  const nextProduct = () => {
    setCurrentProductIndex((prevIndex) => (prevIndex + 1) % products.length);
  };

  const prevProduct = () => {
    setCurrentProductIndex((prevIndex) =>
      prevIndex === 0 ? products.length - 1 : prevIndex - 1
    );
  };

  const currentProduct = products[currentProductIndex];

  return (
    <div className="flex flex-col items-center h-full gap-4">
      <div className="max-h-screen">
        <Product {...currentProduct} />
      </div>
      <div className="flex gap-4 mt-4">
        <Button onClick={prevProduct}>Предыдущий товар</Button>
        <Button onClick={nextProduct}>Следующий товар</Button>
      </div>
    </div>
  );
};

export default ProductsPage;
