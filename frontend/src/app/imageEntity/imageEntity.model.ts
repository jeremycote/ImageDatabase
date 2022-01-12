export class ImageEntity {
    constructor(
        public filename: string,
        public description: string,
        public _id?: number,
        public updatedAt?: Date,
        public createdAt?: Date
    ) {}
}